import spacy
from spacy import displacy
import glob
from tqdm import tqdm
import re



 

def get_entities(sent):
    #prv tok dep和prv tok text将分别保留句子中前一个单词和前一个单词本身的依赖标签。前缀和修饰符将保存与主题或对象相关的文本。
    ent1 = ""
    ent2 = ""


    prv_tok_dep = "" # dependency tag of previous token in the sentence
    prv_tok_text = "" # previous token in the sentence


    prefix = ""
    modifier = ""
    
    for tok in nlp(sent):

        # 接下来，我们将遍历句子中的记号。我们将首先检查标记是否为标点符号。如果是，那么我们将忽略它并转移到下一个令牌。如果标记是复合单词的一部分(dependency tag = compound)，我们将把它保存在prefix变量中。复合词是由多个单词组成一个具有新含义的单词(例如“Football Stadium”, “animal lover”)。
        # 当我们在句子中遇到主语或宾语时，我们会加上这个前缀。我们将对修饰语做同样的事情，例如“nice shirt”, “big house”


        # if token is a punctuation mark then move on to the next token
        if tok.dep_ != "punct":
            # check: token is a compound word or not
            
            if tok.dep_.find("compound") != -1:
                prefix = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep.find("compound") != -1:
                    prefix = prv_tok_text + " "+ tok.text
        
            # check: token is a modifier or not
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep.find("compound")  != -1:
                    modifier = prv_tok_text + " "+ tok.text
        

            # 在这里，如果令牌是主语，那么它将作为ent1变量中的第一个实体被捕获。变量如前缀，修饰符，prv tok dep，和prv tok文本将被重置。
            if tok.dep_.find("subj")  != -1:
                ent1 = modifier +" "+ prefix + " "+ tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = "" 


            # 在这里，如果令牌是宾语，那么它将被捕获为ent2变量中的第二个实体。变量，如前缀，修饰符，prv tok dep，和prv tok文本将再次被重置。
            if tok.dep_.find("obj")  != -1:
                ent2 = modifier +" "+ prefix +" "+ tok.text
    

            # 更新前面的标记和它的依赖标记。
        prv_tok_dep = tok.dep_
        prv_tok_text = tok.text


    return [ent1.strip(), ent2.strip()]

def get_relation(sent):


    doc = nlp(sent)


    # Matcher class object 
    matcher = spacy.matcher.Matcher(nlp.vocab)


    #define the pattern 
    patterns = [{'DEP':'ROOT'}, 
                {'DEP':'prep','OP':"?"},
                {'DEP':'agent','OP':"?"},  
                {'POS':'ADJ','OP':"?"}] 


    matcher.add("matching_1", [patterns]) 


    matches = matcher(doc)
    k = len(matches) - 1


    span = doc[matches[k][1]:matches[k][2]] 


    return(span.text)




nlp = spacy.load("zh_core_web_sm")
path = './txt/*.txt'

patterns = r'，|。|？|！|（|）'

entity_pairs = []
relations=[]

for file in glob.glob(path):
    with open(file, 'r', encoding='utf-8', errors='ignore') as file_in:
        text = file_in.read()
        #print(text)
        text=text.replace('\n','')
        lines = re.split(patterns,text)
        print(lines)
        for line in tqdm(lines):
            print(line)
            if line!='':
                doc=nlp(line)
                for token in doc:
                    #print(token.text,token.pos_,token.tag_)
                    print(token.text,token.dep_,token.head)
                                
                entity_pairs.append(get_entities(i))
                relations.append(get_relation(i))
                print(get_entities(line))
                print(get_relation(line))

# extract subject
source = [i[0] for i in entity_pairs] 
# extract object
target = [i[1] for i in entity_pairs] 



kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})  

# create a directed-graph from a dataframe
G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())  

G=nx.from_pandas_edgelist(kg_df[kg_df['edge']=="composed by"], "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(12,12))
pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
plt.show()

'''
text = '西门子将努力参与中国的三峡工程建设。'
doc = nlp(text)
for token in doc:
  #print(token.text,token.pos_,token.tag_)
  print(token.text,token.dep_,token.head)
#displacy.render(doc,type='dep')
#for ent in doc.ents:
#    print(ent.text, ent.label_)
'''