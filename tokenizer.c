#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct {
    unsigned char *bytes;
    int32_t len;
} Token;


int main() {
    FILE *f = fopen("tok.bin", "rb");     // "rb" = read binary
    if (f == NULL) { printf("can't open\n"); return 1; }

    int32_t a;
    int32_t b;

    // read haader 756 , 500


    fread(&a, sizeof(int32_t), 1, f);     // read 1 int32 into a
    fread(&b, sizeof(int32_t), 1, f);    // continues where the last read stopped

    int32_t *arr = malloc(a * sizeof(int32_t));

    // for loop
    // read size
    // malloc size
    // read bytes

    Token *vocab = malloc(a * sizeof(Token));

    for(int i = 0 ; i < a; i++){
        fread(&vocab[i].len, sizeof(int32_t),1,f);
        vocab[i].bytes = malloc(vocab[i].len);
        fread(vocab[i].bytes,1,vocab[i].len,f);
    }

    printf("%d\n",vocab[507].len);
    fwrite(vocab[507].bytes, 1, vocab[507].len, stdout);
    printf("\n");

    //printf("%d %d\n", a, b);


    //for(int i = 0;i < len())



    fclose(f);
    return 0;
}
