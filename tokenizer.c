#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct {
    unsigned char *bytes;
    int32_t len;
} Token;

typedef struct {
    int32_t x;
    int32_t y;
} Merge;

typedef struct {
    int32_t vocab_size;
    int32_t num_merges;
    Token *vocab;
    Merge *merges;
} Tokenizer;


void dataloader(Tokenizer *t,const char *path){
    FILE *f = fopen(path, "rb");
    if (f == NULL) {
        printf("can't load token data binary file\n");
        return;
    }

    int32_t a;
    int32_t b;
    fread(&a, sizeof(int32_t), 1, f);     // size of vocab
    fread(&b, sizeof(int32_t), 1, f);
    t->vocab_size = a;
    t->num_merges = b;
    printf("vocab_size=%d num_merges=%d\n", t->vocab_size, t->num_merges);
    t->vocab = malloc(t->vocab_size * sizeof(Token));
    t->merges = malloc(t->num_merges * sizeof(Merge));

    for(int i = 0 ; i < a; i++){
        fread(&t->vocab[i].len, sizeof(int32_t),1,f);
        t->vocab[i].bytes = malloc(t->vocab[i].len);
        fread(t->vocab[i].bytes,1,t->vocab[i].len,f);
    }


    fread(t->merges, sizeof(Merge), t->num_merges, f);

    fclose(f);
}

void tokenizer_free(Tokenizer *t) {
    for (int i = 0; i < t->vocab_size; i++) {
        free(t->vocab[i].bytes);
    }
    free(t->vocab);
    free(t->merges);
}

int main() {

    Tokenizer tok;
    dataloader(&tok, "tok.bin");

    // tests
    printf("%d\n",tok.vocab[507].len);
    fwrite(tok.vocab[507].bytes, 1, tok.vocab[507].len, stdout);
    printf("\n");

    printf("%d %d\n",tok.merges[499].x,tok.merges[499].y);

    tokenizer_free(&tok);
    return 0;
}
