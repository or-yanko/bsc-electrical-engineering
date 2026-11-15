/* ex2.c - Student union elections
 * Input : univ00.txt ... univ99.txt (up to 100 files), read ONLY with readFile.
 * Output: 0.txt ... 9.txt, canceled.txt, written ONLY with writeFile,
 *         plus a summary printed to the console.
 * Assumptions: each input file has up to 100 lines; each candidate gets up to
 *         100 valid votes; canceled.txt has up to 100 lines.
 * Do NOT change readFile, writeFile, the required function signatures or the
 * existing struct fields (you may ADD fields to the structs).
 * Do not use FILE, fopen, fscanf, fgets, fprintf, fclose etc. directly.
 * Declare the big arrays (of university / output) static. */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LINES 100
#define MAX_UNIVS 100
#define NUM_CANDIDATES 10

/* ---- provided functions (do not change) ---- */
int readFile(char *filename, char text[][256], int *size)
{
    FILE *fp;
    int i;
    if ((fp = fopen(filename, "r")) == NULL)
        return 0;
    for (i = 0; fgets(text[i], 255, fp); i++)
        text[i][strlen(text[i]) - 1] = '\0';
    *size = i;
    fclose(fp);
    return 1;
}

int writeFile(char *filename, char text[][256], int size)
{
    FILE *fp;
    int i;
    if ((fp = fopen(filename, "w")) == NULL)
        return 0;
    for (i = 0; i < size; i++)
        fprintf(fp, "%s\n", text[i]);
    fclose(fp);
    return 1;
}

/* One vote record (one line of a university file) */
typedef struct student
{
    char name[31];
    char id[10];
    char lastCode, lastNum; /* vote type ('1' head, '2' member) and candidate */
} studentVote;

/* One university file */
typedef struct university
{
    char text[MAX_LINES][256]; /* filled by readFile */
    int size;                  /* number of lines */
} university;

/* One output file */
typedef struct output
{
    char text[MAX_LINES][256];
    int size;
} output;

/* ---- required functions (signatures are checked automatically) ---- */
void loadUniversities(university univs[]);
void parseRecord(const char *line, studentVote *s);
void processVotes(university univs[], output candidates[], output *canceled,
                  int votes[2][NUM_CANDIDATES]);
void writeOutputs(output candidates[], output *canceled);
void printSummary(int votes[2][NUM_CANDIDATES]);

int main(void)
{
    static university univs[MAX_UNIVS];
    static output candidates[NUM_CANDIDATES];
    static output canceled;
    int votes[2][NUM_CANDIDATES] = {0};

    loadUniversities(univs);
    processVotes(univs, candidates, &canceled, votes);
    writeOutputs(candidates, &canceled);
    printSummary(votes);

    return 0;
}

/*==============functions===========*/

void loadUniversities(university univs[])
{
    char filename[] = "univ00.txt";
    char univ_name[] = "univ00";
    int i;

    printf("Voting universities:\n");
    printf("=====================\n");
    for (i = 0; i < MAX_UNIVS; i++)
    {
        filename[4] = '0' + (i / 10);
        filename[5] = '0' + (i % 10);
        univ_name[4] = filename[4];
        univ_name[5] = filename[5];

        univs[i].size = 0;
        if (readFile(filename, univs[i].text, &univs[i].size) == 1)
        {
            printf("%s\n", univ_name);
        }
    }
    printf("----------\n");
}

void parseRecord(const char *line, studentVote *s)
{
    int i;
    for (i = 0; i < 30; i++)
    {
        s->name[i] = line[i];
    }
    s->name[30] = '\0';
    for (i = 0; i < 9; i++)
    {
        s->id[i] = line[30 + i];
    }
    s->id[9] = '\0';
    s->lastCode = line[39];
    s->lastNum = line[40];
}

void processVotes(university univs[], output candidates[], output *canceled,
                  int votes[2][NUM_CANDIDATES])
{
    int indices[MAX_UNIVS] = {0};
    studentVote sv;
    int i, j, k;

    for (i = 0; i < NUM_CANDIDATES; i++)
    {
        candidates[i].size = 0;
        votes[0][i] = 0;
        votes[1][i] = 0;
    }
    canceled->size = 0;

    while (1)
    {
        char min_id[15] = "";
        int has_more = 0;

        studentVote st_votes[4];
        int st_count = 0;
        int voted_in_univs = 0;
        int head_votes = 0;
        int mem_votes = 0;
        int cand_counts[NUM_CANDIDATES] = {0};
        char error_code = '0';

        for (i = 0; i < MAX_UNIVS; i++)
        {
            if (indices[i] < univs[i].size)
            {
                parseRecord(univs[i].text[indices[i]], &sv);
                if (!has_more || strcmp(sv.id, min_id) < 0)
                {
                    strcpy(min_id, sv.id);
                    has_more = 1;
                }
            }
        }

        if (!has_more)
            break;

        for (i = 0; i < MAX_UNIVS; i++)
        {
            int voted_here = 0;
            while (indices[i] < univs[i].size)
            {
                parseRecord(univs[i].text[indices[i]], &sv);
                if (strcmp(sv.id, min_id) == 0)
                {
                    if (st_count < 4)
                    {
                        st_votes[st_count] = sv;
                    }
                    st_count++;
                    voted_here = 1;
                    indices[i]++;

                    if (sv.lastCode == '1')
                        head_votes++;
                    else if (sv.lastCode == '2')
                        mem_votes++;

                    if (sv.lastNum >= '0' && sv.lastNum <= '9')
                        cand_counts[sv.lastNum - '0']++;
                }
                else
                {
                    break;
                }
            }
            if (voted_here)
                voted_in_univs++;
        }

        if (voted_in_univs > 1)
        {
            error_code = '1';
        }
        else if (head_votes > 1 || mem_votes > 2)
        {
            error_code = '2';
        }
        else
        {
            for (j = 0; j < NUM_CANDIDATES; j++)
            {
                if (cand_counts[j] > 1)
                {
                    error_code = '3';
                    break;
                }
            }
        }

        if (error_code != '0')
        {
            for (j = 0; j < 9; j++)
                canceled->text[canceled->size][j] = min_id[j];
            canceled->text[canceled->size][9] = error_code;
            canceled->text[canceled->size][10] = '\0';
            canceled->size++;
        }
        else
        {
            for (j = 0; j < st_count; j++)
            {
                int c_idx = st_votes[j].lastNum - '0';
                for (k = 0; k < 9; k++)
                    candidates[c_idx].text[candidates[c_idx].size][k] = min_id[k];
                candidates[c_idx].text[candidates[c_idx].size][9] = st_votes[j].lastCode;
                candidates[c_idx].text[candidates[c_idx].size][10] = '\0';
                candidates[c_idx].size++;

                if (st_votes[j].lastCode == '1')
                    votes[0][c_idx]++;
                else if (st_votes[j].lastCode == '2')
                    votes[1][c_idx]++;
            }
        }
    }
}
void writeOutputs(output candidates[], output *canceled)
{
    char filename[] = "0.txt";
    int i;
    for (i = 0; i < NUM_CANDIDATES; i++)
    {
        filename[0] = '0' + i;
        writeFile(filename, candidates[i].text, candidates[i].size);
    }
    writeFile("canceled.txt", canceled->text, canceled->size);
}

void printSummary(int votes[2][NUM_CANDIDATES])
{
    int max_head = 0, head_count = 0;
    int max_mem1 = 0, max_mem2 = 0;
    int mem1_count = 0, mem2_count = 0;
    int i;

    /* --------------calc voting for the head-------------- */
    for (i = 0; i < NUM_CANDIDATES; i++)
    {
        if (votes[0][i] > max_head)
            max_head = votes[0][i];
    }

    for (i = 0; i < NUM_CANDIDATES; i++)
    {
        if (votes[0][i] == max_head && max_head > 0)
            head_count++;
    }

    /* --------------printing head results-------------- */
    if (max_head == 0)
    {
        printf("There were no votes for the head.\n");
    }
    else if (head_count == 1)
    {
        for (i = 0; i < NUM_CANDIDATES; i++)
        {
            if (votes[0][i] == max_head)
                printf("There is only one elected head, #%d with %d votes.\n", i, max_head);
        }
    }
    else
    {
        printf("There were more than one elected head:\n");
        for (i = 0; i < NUM_CANDIDATES; i++)
        {
            if (votes[0][i] == max_head)
                printf("%d\n", i); /* הוסרה הסולמית מההדפסה */
        }
        printf("with %d votes.\n", max_head);
    }

    printf("----------\n");

    /* --------------calc voting for the members-------------- */
    for (i = 0; i < NUM_CANDIDATES; i++)
    {
        if (votes[1][i] > max_mem1)
            max_mem1 = votes[1][i];
    }

    for (i = 0; i < NUM_CANDIDATES; i++)
    {
        if (votes[1][i] == max_mem1 && max_mem1 > 0)
            mem1_count++;
    }

    if (max_mem1 == 0)
    {
        printf("There were no votes for the member.\n");
    }
    else if (mem1_count > 1)
    {
        printf("There were more than one elected for member1:\n");
        for (i = 0; i < NUM_CANDIDATES; i++)
        {
            if (votes[1][i] == max_mem1)
                printf("%d\n", i); /* הוסרה הסולמית מההדפסה */
        }
        printf("with %d votes.\n", max_mem1);
    }
    else
    {
        for (i = 0; i < NUM_CANDIDATES; i++)
        {
            if (votes[1][i] == max_mem1)
            {
                printf("There is only one elected for member1, #%d with %d votes.\n", i, max_mem1);
            }
        }

        for (i = 0; i < NUM_CANDIDATES; i++)
        {
            if (votes[1][i] > max_mem2 && votes[1][i] < max_mem1)
            {
                max_mem2 = votes[1][i];
            }
        }

        for (i = 0; i < NUM_CANDIDATES; i++)
        {
            if (votes[1][i] == max_mem2 && max_mem2 > 0)
            {
                mem2_count++;
            }
        }

        /* --------------printing members results-------------- */
        if (max_mem2 == 0)
        {
            printf("There were no votes for member2.\n");
        }
        else if (mem2_count == 1)
        {
            printf("----------\n");
            for (i = 0; i < NUM_CANDIDATES; i++)
            {
                if (votes[1][i] == max_mem2)
                {
                    printf("There is only one elected for member2, #%d with %d votes.\n", i, max_mem2);
                }
            }
        }
        else
        {
            printf("----------\n");
            printf("There were more than one elected for member2:\n");
            for (i = 0; i < NUM_CANDIDATES; i++)
            {
                if (votes[1][i] == max_mem2)
                    printf("%d\n", i); /* הוסרה הסולמית מההדפסה */
            }
            printf("with %d votes.\n", max_mem2);
        }
    }

    printf("----------\n");
}