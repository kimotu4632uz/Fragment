extern crate regex;
extern crate exif;
extern crate failure;

use regex::Regex;
use exif::{Reader, Tag};

use std::fs;
use std::path::{Path, PathBuf};
use std::io;
use std::vec::Vec;
use std::default::Default;
use std::string::String;
use std::env;
use std::ffi::OsString;

fn find<P: AsRef<Path>>(p: P) -> io::Result<Vec<PathBuf>> {
    let path: &Path = p.as_ref();
    let t = path.metadata()?.file_type();

    if t.is_file() { Ok(vec![path.to_path_buf()]) }
    else if t.is_dir() {
        let mut acc = vec![];
        for x in fs::read_dir(path)? {
            acc.append(&mut find(x.unwrap().path())?);
        }
        Ok(acc)
    } else { Ok(vec![]) }
}

fn rename<P: AsRef<Path>>(p: P) -> Result<PathBuf, failure::Error> {
	let path: &Path = p.as_ref();
    let file = fs::File::open(path)?;
    let reader = Reader::new(&mut io::BufReader::new(&file))?;
    
    let date = reader.get_field(Tag::DateTimeOriginal, false).unwrap().value.display_as(Tag::DateTimeOriginal);
    let name: String = format!("{}", date).chars().filter(|x| x.is_numeric()).collect();
    let ext  = path.extension().map_or(Default::default(), |x| format!(".{}", x.to_str().unwrap()));
    
    Ok(path.with_file_name(format!("{}{}", name, ext)))
}

fn main() -> Result<(), failure::Error> {
	let args: Vec<OsString> = env::args_os().collect();
	let txt = fs::read_to_string("rules.txt");
	println!("{:?}",txt);
    let re = Regex::new(r"DSC_\d.JPG")?;
    
    let matched: Vec<(PathBuf, PathBuf)>
      = find(&args[1])?.into_iter()
        .filter(|x| re.is_match(& x.file_name().unwrap().to_str().unwrap()))
        .map(|x| (x.clone(), rename(x).unwrap())).collect();
    
    if matched.is_empty() {
        println!("nothing to do.");
    } else {
        println!("rename as:");
        for (x,y) in matched {
            println!("{} -> {}", x.display(), y.display());
            fs::rename(x,y)?;
        }
    }
    Ok(())
}

