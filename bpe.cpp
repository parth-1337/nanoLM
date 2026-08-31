#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <fstream>
#include <sstream>
#include <random>
#include <cmath>

//class bpe
// has tokenizer function and before that the merging train data merges maker


class Tokenizer {
    public :
        std::map< std::pair <int, int>, int> merges;
        int next_token_id = 256; // initial 0-255 raw bytes

        // main training loop
        void train (std::string& path, int num_merges){
            std::ifstream file(path, std::ios::binary);
            if(!file){
                std::cerr<<" error in openeing training file";
            }
            std::vector<int> tokens;
            char byte;
            while (file.get(byte)) {
                tokens.push_back(static_cast<unsigned char>(byte));
            }
            file.close();

            for(int i = 0; i < num_merges; ++i) {
                //find most pair
                std::map< std::pair<int, int>, int> count_pair;
                for(size_t i = 0; i < tokens.size() - 1; ++i){
                    count_pair[{tokens[i] ,tokens[i+1]}]++;
                }

            }

        }
};


int main(){
    Tokenizer tokenize ;
    tokenize.train("training_data.txt", 500)

    return 0;
}
