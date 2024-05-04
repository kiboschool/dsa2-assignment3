import os
import re
import heapq

class FileAnalyzer:
    def __init__(self):
        # The inverted index, which maps words (strings) to heaps.
        # Each heap is represented as a list of tuples, where each
        # tuple represents information about the occurrences of that
        # word in a document.
        #
        # For example:
        # 'hello' -> [ (5, 'example1.txt', [ <lines where 'hello' appears)],
        #              (3, 'example2.txt', [ <lines where 'hello' appears)],
        #              ... ]
        self.index = {}

    # Task 1
    def heapify_example(self):
        return [
            [2, 10, 25, 5, 12, 16, 28]
            # Three other iterations of heap construction here:
        ]

    # Task 2
    def add_document(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            word_freqs = {}

            for line in file:
                # Convert to lowercase and remove commas, periods, and newlines
                cleaned_line = re.sub(r'[,.\n]', '', line.lower())
                words = cleaned_line.split()

                for word in words:
                    if word not in word_freqs:
                        word_freqs[word] = (1, [line])
                    else:
                        freq, lines = word_freqs[word]
                        lines.append(line)
                        word_freqs[word] = (freq + 1, lines)

            for word, tup in word_freqs.items():
                freq, lines = tup
                if word not in self.index:
                    self.index[word] = [(-freq, filename, lines)]
                else:
                    heapq.heappush(self.index[word], (-freq, filename, lines))

    # Task 3
    def top_k_documents(self, word, k):
        if word not in self.index:
            return []

        lst = []
        for i in range(k):
            lst.append(heapq.heappop(self.index[word]))

        ret = [filename for _, filename, _ in lst]

        for entry in lst:
            heapq.heappush(self.index[word], entry)

        return ret

    # Task 4
    def top_k_contexts(self, word, k):
        if word not in self.index:
            return []

        found = 0
        lst = []
        ret = []
        while found < k:
            lst.append(heapq.heappop(self.index[word]))
            lines = lst[-1][2]
            i = 0
            while found < k and i < len(lines):
                ret.append(lines[i])
                found += 1
                i += 1

        for entry in lst:
            heapq.heappush(self.index[word], entry)

        return ret

    # Task 5
    def similarity_score(self, str1, str2, memo={}):
        if (str1, str2) in memo:
            return memo[(str1, str2)]

        # Base cases: If one of the strings is empty,
        # return the length of the other string
        if len(str1) == 0:
            return len(str2)
        if len(str2) == 0:
            return len(str1)

        # If the first characters of the strings are the same,
        # no operation is needed
        if str1[0] == str2[0]:
            return self.similarity_score(str1[1:], str2[1:], memo)

        # Otherwise, find the minimum of three operations:
        # insert, delete, or replace
        insert_cost = self.similarity_score(str1, str2[1:], memo)
        delete_cost = self.similarity_score(str1[1:], str2, memo)
        replace_cost = self.similarity_score(str1[1:], str2[1:], memo)

        memo[(str1, str2)] = min(insert_cost, delete_cost, replace_cost) + 1
        return memo[(str1, str2)]

    # Note: you should not modify this function.
    def document_similarity(self, file1, file2):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            content1 = f1.read()[:250]
            content2 = f2.read()[:250]
        return self.similarity_score(content1, content2)

    # Note: you should not modify this function.
    def document_similarities(self, folder_path):
        print('\nNote: the similarity score calculation will not work efficiently until Task 5 is completed.')
        files = os.listdir(folder_path)
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                print('  Similarity score between ' + files[i] + ' and ' + files[j] + ': ', end='', flush=True)
                print(self.document_similarity(os.path.join(folder_path, files[i]), os.path.join(folder_path, files[j])))

# Example usage.
if __name__ == "__main__":
    analyzer = FileAnalyzer()
    analyzer.add_document('examples/example1.txt')
    analyzer.add_document('examples/example2.txt')
    analyzer.add_document('examples/example3.txt')
    analyzer.add_document('examples/example4.txt')
    print(analyzer.top_k_documents('earthquake', 3))
    print(analyzer.top_k_contexts('earthquake', 5))
    analyzer.document_similarities('examples')
