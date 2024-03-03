#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *sound = fopen(argv[1], "rb");

    // Read header
    // TODO #3
    BYTE b;
    int header_quantity = 0;

    WAVHEADER header;

    fread(header.chunkID, sizeof(BYTE), 4, sound);

    fread(&header.chunkSize, sizeof(header.chunkSize), 1, sound);

    fread(header.format, sizeof(BYTE), 4, sound);

    fread(header.subchunk1ID, sizeof(BYTE), 4, sound);

    fread(&header.subchunk1Size, sizeof(header.subchunk1Size), 1, sound);

    fread(&header.audioFormat, sizeof(header.audioFormat), 1, sound);

    fread(&header.numChannels, sizeof(header.numChannels), 1, sound);

    fread(&header.sampleRate, sizeof(header.sampleRate), 1, sound);

    fread(&header.byteRate, sizeof(header.byteRate), 1, sound);

    fread(&header.blockAlign, sizeof(header.blockAlign), 1, sound);

    fread(&header.bitsPerSample, sizeof(header.bitsPerSample), 1, sound);

    fread(header.subchunk2ID, sizeof(BYTE), 4, sound);

    fread(&header.subchunk2Size, sizeof(header.subchunk2Size), 1, sound);

    // Use check_format to ensure WAV format
    // TODO #4
    check_format(header);

    // Open output file for writing
    // TODO #5
    FILE *copy = fopen(argv[2], "wb");

    // Write header to file
    // TODO #6

    fwrite(header.chunkID, sizeof(BYTE), 4, copy);

    fwrite(&header.chunkSize, sizeof(header.chunkSize), 1, copy);

    fwrite(header.format, sizeof(BYTE), 4, copy);

    fwrite(header.subchunk1ID, sizeof(BYTE), 4, copy);

    fwrite(&header.subchunk1Size, sizeof(header.subchunk1Size), 1, copy);

    fwrite(&header.audioFormat, sizeof(header.audioFormat), 1, copy);

    fwrite(&header.numChannels, sizeof(header.numChannels), 1, copy);

    fwrite(&header.sampleRate, sizeof(header.sampleRate), 1, copy);

    fwrite(&header.byteRate, sizeof(header.byteRate), 1, copy);

    fwrite(&header.blockAlign, sizeof(header.blockAlign), 1, copy);

    fwrite(&header.bitsPerSample, sizeof(header.bitsPerSample), 1, copy);

    fwrite(header.subchunk2ID, sizeof(BYTE), 4, copy);

    fwrite(&header.subchunk2Size, sizeof(header.subchunk2Size), 1, copy);

    // Use get_block_size to calculate size of block
    // TODO #7
    int block_size = get_block_size(header);

    // Write reversed audio to file
    // TODO #8

    BYTE *bit = malloc(block_size);

    int samples = header.subchunk2Size;

    fseek(sound, -block_size, SEEK_END);
    while (samples > 0)
    {
        fread(bit, sizeof(BYTE), block_size, sound);
        fwrite(bit, sizeof(BYTE), block_size, copy);
        fseek(sound, -(block_size * 2), SEEK_CUR);

        samples -= block_size;
    }

    free(bit);
    fclose(sound);
    fclose(copy);
}

int check_format(WAVHEADER header)
{
    char *wave = "WAVE";
    char *waveConfirm = malloc(strlen(wave) + 1);

    for (int i = 0; i < strlen(wave); i++)
    {
        waveConfirm[i] = header.format[i];
    }

    waveConfirm[strlen(wave)] = '\0';

    if (strcmp(wave, waveConfirm) == 0)
    {
        free(waveConfirm);
        return 1;
    }

    free(waveConfirm);
    return 0;
}

int get_block_size(WAVHEADER header)
{

    int block_size = header.numChannels * (header.bitsPerSample / 8);

    return block_size;
}
