#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <discid/discid.h>

typedef struct {
  char ident;
  char *long_opt;
  char *help;
} Option;

static Option optdict[] = {
  { 'h', "--help", "show help" },
  { 'm', "--music-brainz", "show MBID" },
  { 'f', "--freedb", "show FreeDB disc id" },
  { 'i', "--isrc", "show ISRC of each track" },
  { 't', "--toc", "show TOC string; format: (first track number) (last track number) (total length in sectors) (offset of 1st track) (offset of 2nd track)..." },
  { 0, NULL, NULL }
};

void print_help() {
  printf("Usage: discid.exe [OPTIONS]\n\n");
  printf("Options:\n");
  for (int i = 0; optdict[i].ident != 0; i++)
    printf("  -%c, %s   %s\n", optdict[i].ident, optdict[i].long_opt, optdict[i].help);
}

char optcmp(const char* arg) {
  for (int i = 0; optdict[i].ident != 0; i++) {
    char short_opt[] = { '-', optdict[i].ident, '\0' };

    if (strcmp(arg, short_opt) == 0 || strcmp(arg, optdict[i].long_opt) == 0)
      return optdict[i].ident;
  }

  return 0;
}

int32_t argparse(int argc, const char *argv[]) {
  int32_t flag = 0;

  for (int i = 1; i < argc; i++) {
    switch (optcmp(argv[i])) {
      case 'h':
        return 0;
      
      case 'm':
        flag |= 0b0001;
        break;
      
      case 'f':
        flag |= 0b0010;
        break;

      case 'i':
        flag |= 0b0100;
        break;
      
      case 't':
        flag |= 0b1000;
        break;

      default:
        break;
    }
  }

  return flag;
}

int main(int argc, const char *argv[]) {
  int32_t flag = 0b1111;

  if (argc > 1) flag = argparse(argc, argv);
  if (flag == 0) {
    print_help();
    return 0;
  }

  DiscId *disc = discid_new();

  if (discid_read(disc, NULL) == 0) {
    printf("Error: %s\n", discid_get_error_msg(disc));
    discid_free(disc);
    return 1;
  }

  if ((flag & 0b1) == 0b1) {
    if (flag == 0b1)
      printf("%s\n", discid_get_id(disc));
    else
      printf("MusicBraiz disc id: %s\n", discid_get_id(disc));
  }

  if ((flag & 0b10) == 0b10) {
    if (flag == 0b10)
      printf("%s\n", discid_get_freedb_id(disc));
    else
      printf("FreeDB disc id:     %s\n", discid_get_freedb_id(disc));
  }

  if ((flag & 0b100) == 0b100) {
    int first = discid_get_first_track_num(disc);
    int last = discid_get_last_track_num(disc);

    for (int i = first; i <= last; i++) {
      printf("ISRC of track %d: %s\n", i, discid_get_track_isrc(disc, i));
    }
  }

  if ((flag & 0b1000) == 0b1000) {
    if (flag == 0b1000)
      printf("%s\n", discid_get_toc_string(disc));
    else
      printf("TOC: %s\n", discid_get_toc_string(disc));
  }

  discid_free(disc);
  return 0;
}
