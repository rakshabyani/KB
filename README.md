# KB - 
●	Programmed an engine in Python for parsing knowledge bases with first order logic statements
●	Used resolution inference algorithm to prove logical queries.

Problem Description:
Dr. Ernest Beakerman has been experimenting with gene knockout mice for the last 10 years. Recently he has had a major breakthrough with his KM-52a strain. It turns out that the mice are hyper intelligent and possess a keen grasp of logic far superior to any human. Since mice by their nature are quite friendly the KM-52a mice have employed themselves to bettering humanity. For instance, Algernon II is now advising the president on foreign matters and has brought the ISIS crisis to a graceful ending and stopped the spread of AIDS in Africa.
The problem with KM-52a is that, like all other mice, they live at most 4 years. As a result, new generations must be constantly trained to replace the current mice, which die off very quickly. Additionally, they must be trained with great speed so that they can spend as much time as possible aiding humanity into a new era of prosperity.
Dr. Beakerman has employed you in his lab to facilitate the training of KM-52a mice. Each mouse will sit in front of a computer practicing logic exercises. It will be presented with several first-order logic statements. It will read them and then type in a logical query, which the statements should be able to prove. Your job is to write a program that will check each conclusion a mouse makes and give it immediate feedback as to whether the query can be proven. Thus, the mice will learn very quickly via feedback a strong understanding of logic.
To help you develop your system, Dr Beakerman has provided you with several sample knowledge bases the mice have produced. The knowledge bases contain sentences with the following defined operators:
NOT X
X OR Y
X AND Y
X IMPLIES Y
~X
X | Y X & Y X => Y


Used the resolution inference algorithm, full first-order version to solve this problem.
Once this project is completed, Dr. Beakerman will use it to expedite the training of KM-52a mice and thus usher in a new era of peace and prosperity. After that he will collect his Nobel prize and from then on forget to ever mention your name when talking about how to train KM-52a mice.
Format for input.txt:
<NQ = NUMBER OF QUERIES>
<QUERY 1>
...
<QUERY NQ>
<NS = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE>
<SENTENCE 1>
...
<SENTENCE NS>
where
• Each query will be a single literal of the form Predicate(Constant) or ~Predicate(Constant).
• Variables are all single lowercase letters.
• All predicates (such as Sibling) and constants (such as John) are case-sensitive alphabetical strings that
begin with an uppercase letter.
• Each predicate takes at least one argument. Predicates will take at most 100 arguments. A given
predicate name will not appear with different number of arguments.
• There will be at most 100 queries and 1000 sentences in the knowledge base.
• See the sample input below for spacing patterns.
• You can assume that the input format is exactly as it is described. There will be no syntax errors in the
given input.
Format for output.txt:
For each query, determine if that query can be inferred from the knowledge base or not, one query per line:
<ANSWER 1>
...
<ANSWER NQ>
where
each answer should be either TRUE if you can prove that the corresponding query sentence is true given the knowledge base, or FALSE if you cannot.
