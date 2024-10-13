# Assignment 3

In this assignment, you will complete a series of exercises with heaps and dynamic programming to implement a file analyzer. The analyzer will allow users to efficiently search for words in documents and compute similarity scores between documents.

## Your Task

You are given a partial implementation of a `FileAnalyzer` class that provides various functionality related to heaps, dynamic programming, and analyzing files.

Task 1 will ask you to show the steps of converting an arbitrary list to a heap.

Tasks 2, 3, and 4 will have you implement an [inverted index](https://en.wikipedia.org/wiki/Inverted_index), a data structure that allows us to efficiently lookup words to find which document(s) those words appear in. You will first write the code to populate the inverted index given the documents, and then write algorithms to show the top `k` documents for a given word (by frequency), as well as showing `k` lines of text where the word appears in the documents.

Task 5 will have you add memoization to a recursive algorithm that computes a similarity score between two documents. The similarity score will show that one of the example documents is a plagiarized copy of one of the other documents!

## Steps to Complete

Complete the following steps to the best of your ability, and with the following guidelines:

* The use of generative AI tools (e.g., ChatGPT) is not permitted.
* You must only use concepts and programming constructs covered in this class or previous Kibo classes.
* The algorithms you write should be as efficient as possible.
* For a heap data structure, you should use the Python `heapq` library. For a hash table, you should use Python dictionaries.

1. Say that we have the following list of numbers: `[2, 10, 25, 5, 12, 16, 28]`. Show how this list could be converted into a valid max-at-top heap following the `O(n)` heap construction algorithm for an existing list as discussed in class.

    Implement your answer in the `heapify_example()` function as a two-dimensional list. The first sublist in the list should be the starting list above. You should then add one sublist to the list for every iteration of the heap construction algorithm to show the state of the list after each sift is completed.

    Notes:

    * Since in the list above you will need to perform three iterations sifting, your answer should be a 2D list with four sublists: one for the starting state of the list, and one to show the evolution of the list after each iteration of the algorithm.

2. Finish implementing the `add_document()` algorithm, which is the first step toward implementing an inverted index. You will continue adding functionality to the inverted index in tasks 3 and 4.

    The `add_document()` method should accept the name of a file as input, and use the words in the file to populate the inverted index. The method already has some code to read in the words of the document, and performs some preprocessing to make all of the words lowercase and strip away punctuation. You should continue implementing the algorithm where the given code ends.

    In particular, you should construct an inverted index by modifying `self.index` (a dictionary). For each word found in the document, `self.index` should be modified to associate that word with a heap, where each element of the heap is a triple of values: `(frequency, document, contexts)`, where

    * `frequency` is the number of times the given word appears in the document
    * `document` is the name (filename) of the document
    * `contexts` is a list of all of the lines on which the word appears in the document. If a word appears multiple times on a given line, that line will appear multiple times in `contexts`.

    For example, here is what the inverted index might look like for the word `'hello'` after several documents have been added:

    <center>
    <img
      src="/images/dsa2-assignment3-inverted-index.svg"
      alt="An inverted index showing that the string hello maps to a heap, where the elements of the heap represent how many times the string hello appears in each document."
      style="width:500px;"
    />
    </center>

    Notes:

    * The items in each heap should be ordered by the word frequency in the documents. They should be max-at-top heaps, meaning the document with the highest frequency of a given word should appear at the top of the heap for that word.
    * You might find it helpful to first iterate over the document in its entirety to build a local dictionary that maps words to (frequency, contexts) pairs. Then, iterate over this local dictionary to populate or maintain the heaps for each word in the index.
    * Remember that we represent heaps as lists, not as linked data structures. Therefore, although the picture above visualizes the heap as a tree structure, `self.index` will actually map each word to a *list* of tuples.
    * To use a heap, you should use the `heapq` library, including the `heappush()` method. You will need to account for the fact that `heapq` implements min-at-top heaps (whereas we need a max-at-top heap).
    * Since `add_document()` can be called multiple times, there may already be entries inside of `self.index` when the method is called.
    * When adding contexts to the inverted index, you should use the raw (unprocessed) version of each line, not the cleaned version.

3. Implement the `top_k_documents()` method, which should fetch and return as a list the top `k` documents for the given word, ordered by frequency.

    For the example inverted index shown above, `top_k_documents('hello', 2)` should return: `['example4.txt', 'example3.txt']`.

    * In order to get the top `k` documents for a given word, you will need to repeatedly pop items off of the heap that corresponds to that word in the index.
    * Before returning from the method, you will need to reset the heap to its original condition, i.e., the `k` items should be pushed back onto the heap.
    * There might be other ways to get the top `k` items off of the heap *without* modifying the heap; you're free to explore those options as well.
    * Your `top_k_documents()` method should run in time `O(k*logn)`, where `k` is the number of items to fetch and `n` is the total number of items on the heap. It should also use only `O(k)` extra space.
    * You should not perform any unnecessary heap removals.

4. Implement the `top_k_contexts()` method, which should fetch and return as a list the top `k` *contexts* for the given word, ordered by the number of times the word appears in documents.

    For example, say we have the following inverted index, which contains a key for `'foo'`:

    <center>
    <img
      src="/images/dsa2-assignment3-inverted-index-contexts.svg"
      alt="An inverted index showing that the string foo maps to a heap, where the elements of the heap represent how many times the string foo appears in each document."
      style="width:475px;"
    />
    </center>

    If `top_k_contexts('foo', 5)` is called, then it should report the top 5 contexts (lines) where `'foo'` appeared in the documents, which would be: `['foo part 1', 'Where is foo?', 'foo bar', 'foo part II', 'foo baz']`. Note that `'boo foo'` is not included, since it would have been the sixth context where `'foo'` appears.

    Notes:

    * If there are less than `k` occurrences of a word between all of the documents in the index, then you should include in the results however many occurrences are available.
    * Just like in `top_k_documents()`, you may remove items from the heap, but you need to put them back into the heap before the algorithm is finished.
    * You should only remove as many items from the heap as is necessary. For example, if you're looking for `k = 5` contexts and the document at the top of the heap has seven occurrences of the word, then you should use the first five occurrences in the results, ignore the last two, and not pop any more entries off of the heap.

5. Currently, the `similarity_score()` algorithm computes a similarity score between two strings to see how similar they are. If the two strings are exactly the same, the algorithm returns 0, meaning that no changes are needed to make the strings equal to each other. However, if they are different, the algorithm calculates the number of insertions, deletions, and/or substitutions that would be needed to make the two strings equal.

   The current function works, but it is inefficient, and therefore can't effectively compute the similarity scores for the documents in our collection.

   Your task is to modify the `similarity_score()` method to add *memoization* to the algorithm, so that the similarity scores can be calculated in a reasonable amount of time (a few seconds).

    Notes:

    * In order for the memoization to work, you should add a new default parameter `memo` that defaults to the empty dictionary: `def similarity_score(self, str1, str2, memo={})`. You should then populate this dictionary with the results of subproblems, and check the dictionary for previously-computed subproblems as needed.
    * Once implemented correctly, the similarity scores between the different documents should be able to be computed within a few seconds.
    * The lower the similarity score, the closer two documents are to being the same.
    * The unit test for `similarity_score()` does not test the efficiency gain you are tasked with making. However,it does test that the output of the function remains correct as you change it. However, the Gradescope Autograder uses timeouts to test for efficiency.
    * The file `examples/example4.txt` is actually a plagiarized article that copies one of the other articles too closely. Can you tell which article it copies, just by looking at the similarity scores? (You don't need to actually respond to this question.)

## Testing

In `test_file_analyzer.py`, there are unit tests for the above pieces of functionality. Run the tests to check your code.

When you upload your submission to Gradescope, you will see the results for some tests, but there may be other edge cases we test during grading that you are not able to see when you submit. So be sure to test thoroughly!
