#include <stdio.h>
#include <utility>

using Size = struct {
    int hight;
    int width;
};

void test(Size& size) {
    Size tmp = {1,4};
    printf("%d\n", tmp.width);
    size = std::move(tmp);
}

void test(Size* size) {
    Size tmp = {1,4};
    printf("%d\n", tmp.width);
    size = &tmp;
}

int main() {
    Size mov;
    Size* ptr = nullptr;
    test(mov);
    //size(ptr); error!
    printf("%d\n", out.width);
    return 0;
}

