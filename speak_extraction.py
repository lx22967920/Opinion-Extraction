# Coding: utf-8
# Time  : 2019/8/21
# Author: Li Xiang
# @Email: 22967920@qq.com
import re
from pyhanlp import *
import math


class SpeakExtraction(object):
    def __init__(self):
        self.speaks = []
        self.sentences = []
        self.speak_to_position = {}
        self.person_to_speak = {}
        self.names = []
        self.names_to_position = {}
        self.segment = HanLP.newSegment().enableNameRecognize(True)

    def name2speak(self, text):
        text = self.clean_text(text)
        print(text)
        self.get_sentences(text)
        self.get_speaks(text)
        self.speak2position(text)
        self.get_names()
        self.name2position(text)
        name_to_speak = []
        if len(self.speaks) == 0:
            print("Speak not found.")
            return
        for speak in self.speak_to_position:
            start_pos = self.speak_to_position[speak][0]
            end_pos = self.speak_to_position[speak][1]
            min_distance = len(speak)
            if not self.names:
                print("No name found.")
                return
            best_name = self.names[0]
            for name in self.names_to_position:
                name_positions = self.names_to_position[name]  # list
                for n in name_positions:
                    distance = min(math.fabs(n - start_pos), math.fabs(n - end_pos))
                    if distance < min_distance:
                        min_distance = distance
                        best_name = name

            name_to_speak.append({best_name: speak})
        return name_to_speak

    def get_sentences(self, text):
        para = re.sub('([。！？])([^”’])', r"\1\n\2", text)
        para = para.split("\n")
        self.sentences = [sent for sent in para if sent]

    def get_speaks(self, text):
        self.speaks.clear()
        temp = re.findall(r"“(.+?)”", text)
        self.speaks = [sen for sen in temp if len(sen) >= 10]
        return self.speaks

    def get_names(self):
        self.names.clear()
        for sent in self.sentences:
            # 将句子中的对话移除，避免对话中出现的人物成为speaker
            for speak in self.speaks:
                sent.replace(speak, "")
            term_list = list(self.segment.seg(sent))
            for item in term_list:
                term, label = str(item).split("/")
                if label == "nr":
                    self.names.append(term)
        return self.names

    def speak2position(self, text):
        self.speak_to_position.clear()
        for speak in self.speaks:
            start_position = text.find(speak)
            end_position = start_position + len(speak)
            self.speak_to_position[speak] = (start_position, end_position)

    def name2position(self, text):
        self.names_to_position.clear()
        for name in self.names:
            index_list = []
            index = text.find(name)
            while index != -1:
                index_list.append(index)
                index = text.find(name, index + 1)
            self.names_to_position[name] = index_list

    @staticmethod
    def clean_text(text):
        text = text.replace("\n", "")
        return text


text = """
新华社北京8月6日电 外交部发言人华春莹6日就美国财政部将中国列为“汇率操纵国”答记者问。有记者问：美国财政部宣布正式将中国列为汇率操纵国，\
为1994年以来首次。中方对此有何回应？是否会有反制措施？华春莹说，中国人民银行已经就美国财政部将中国列为“汇率操纵国”发表了声明。美方不顾事实和自己\
制订的所谓“汇率操纵国”的量化标准，无理给中国贴上“汇率操纵国”的标签，是继8月1日宣布拟对中国3000亿美元商品加征关税后，升级贸易争端的又一恶劣行径。\
“美方这一任性的单边主义和保护主义行为是对国际规则的公然践踏和挑衅，破坏了全球关于汇率问题的多边共识，不仅不利于理性、务实地解决中美经贸问题，还将严重\
破坏国际金融秩序，阻碍国际贸易和全球经济复苏，中方对此坚决反对。”她说。华春莹表示，中国实施的是以市场供求为基础、参考一篮子货币进行调节、有管理的浮动汇\
率制度，在机制上人民币汇率是由市场供求决定的，不存在“汇率操纵”的问题。中方一直致力于维护人民币汇率在合理均衡水平上基本稳定，这一努力国际社会有目共睹。201\
8年以来，美国不断升级贸易争端，多次引发全球金融市场大幅波动，但中方始终坚持不搞竞争性贬值，没有也不会将汇率作为工具来应对贸易争端。华春莹说:“中方敦促美方尽\
快回归理性，纠正错误做法，以免对两国关系造成进一步损害。”
"""
text2 = """
荒谬逻辑尽显霸凌本色——专家批驳美将中国列为“汇率操纵国”

　　新华社记者李延霞、张千千、陈炜伟

　　美国财政部北京时间6日凌晨发布声明，决定将中国列为“汇率操纵国”。对此，专家认为，美国此举逻辑荒谬，是典型的“欲加之罪，何患无辞”，尽显美国霸凌本色。

　　自由裁量 为所欲为

　　“美国此次单方面将中国列为‘汇率操纵国’，从时间上看是对近日人民币汇率贬值的应激反应，实际上连美国自己为‘汇率操纵国’设定的标准都不符合。”东方金诚首席宏观分析师王青表示。

　　根据美国对“汇率操纵国”最新的认定标准，当一国在过去四个季度满足以下三个标准时会被认定为“汇率操纵国”：1.对美国贸易顺差超过200亿美元；2.经常账户顺差占GDP比重超过2%；3.单边汇率干预金额占本国GDP比重2%以上，且持续时长超过6个月。

　　如果一个经济体满足三个标准，则被认定为“汇率操纵国”；如果只满足两个标准，会被列入观察名单；如果只满足第一个标准，但该经济体对美国的总体贸易逆差贡献较大，也可能被列入观察名单。

　　“2018年中国经常账户顺差与GDP之比仅为0.4%左右，2016年下半年至今，中国外汇储备规模一直稳定在3万亿美元左右，根本不存在大规模买入外国资产促使本币贬值的可能。”王青说，即使按照美国自己的标准，将中国列入“汇率操纵国”也是毫无道理的。

　　中国金融四十人论坛高级研究员管涛认为，美国的做法可以说是“欲加之罪，何患无辞”。

　　“正是因为中国不符合美国制定的三项标准，此次美国并没有引用这个标准，而是拿中国人民银行答记者问的内容作为借口。”他表示，美国所谓的“证据”部分，其实是央行对投机者的警告，美国却拿来作为中国操纵汇率的证据，十分可笑。

　　招商证券首席宏观分析师谢亚轩表示，“汇率操纵国”的三项标准是美国自己制定的，在认定上，美国财政部有很大的话语权，可以为了自身利益而随意进行自由裁量。

　　对外经贸大学国际经济研究院院长桑百川认为，美国此举的根本目的是为了配合对华贸易战，使得美国对中国输美商品加征关税的效应达到最大化，是升级贸易战的新手法。

　　他认为，受美国单方面加征关税的影响，市场有担忧情绪，人民币出现一定程度的贬值是市场作用的结果。美国认为中国是“汇率操纵国”，是缺乏依据的，也缺乏经济基础的支撑。

　　双重标准 自相矛盾

　　专家认为，美国在人民币刚刚“破7”这一时间节点就立刻宣布将中国列入“汇率操纵国”，是典型的双重标准。

　　美国此举的一大背景是，受美国单方面加征关税的影响，人民币兑美元离岸和在岸汇率5日双双“破7”。

　　“美国一直要求别国汇率市场化，不干预，但在人民币‘破7’之后，对这样的整数关口却很在意，这是典型的双重标准。”管涛说，美国的这种做法，恐怕只是为其贸易政策找一个借口，可以有理由对中国输美商品加征更多关税。

　　他认为，去年以来人民币汇率多次承压，对外经贸纷争是重要诱因。如果美国不再出尔反尔，妥善解决双方经贸摩擦，市场情绪稳定的话，将为人民币稳定创造良好的环境。

　　以我为主 练好内功

　　专家认为，如果从较长时间的维度看，人民币无论对单边还是双边都是升值的，汇率指数是基本稳定的。人民币属于比较坚挺的货币，不存在用贬值获得产品竞争优势的情况。

　　王青表示，2015年“8·11”汇改后，中国一直致力于加快汇率市场改革步伐，人民币汇率总体上形成了主要由市场力量驱动的双向波动格局。近年来，人民币汇率的波动率在增加，已接近国际主要储备货币的波动率。

　　管涛表示，国际货币基金组织（IMF）承担督促成员国避免货币竞争性贬值的职责。IMF最近发布的报告认为，2018年人民币实际有效汇率与经济基本面保持一致。

　　交通银行首席经济学家连平表示，当前中国经济整体运行平稳，人民币汇率并没有出现持续大幅度贬值的基础和条件，中国经济的基本面，对于支撑汇率的基本稳定会发挥积极作用。

　　“在外部压力加大背景下，中方最重要的事情仍是集中精力把国内的事办好，练好内功，夯实国内宏观经济稳健运行的基础。”王青说。"""

speak_extrac = SpeakExtraction()
speak = speak_extrac.name2speak(text)
speak2 = speak_extrac.name2speak(text2)
print(speak)
print(speak2)

