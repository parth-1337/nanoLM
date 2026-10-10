#include <stdio.h>
#include <stdint.h>

int main() {
    FILE *f = fopen("tok.bin", "rb");     // "rb" = read binary
    if (f == NULL) { printf("can't open\n"); return 1; }

    int32_t a;
    int32_t b;
    int32_t c;
    int32_t d;
    fread(&a, sizeof(int32_t), 1, f);     // read 1 int32 into a
    fread(&b, sizeof(int32_t), 1, f);    // continues where the last read stopped
    fread(&c, sizeof(int32_t), 1, f);
    fread(&d, sizeof(int32_t), 1, f);
    printf("%d %d\n", a, b);
    printf("%d %d\n", c, d);
    fclose(f);
    return 0;
}
