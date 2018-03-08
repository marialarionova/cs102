import math
from scraputils import split_row


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha

    def fit(self, x, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.labels = [i for i in set(y)]  # собираем лейблы good, maybe, never
        self.labels.sort()  # теперь сортируем их
        classes = len(self.labels)  # считаем их количество
        number_of_labels = [0] * classes  # создаём массив из ноликов по кол-ву лейблов
        for i in range(len(y)):  # назначаем лейблам цифровые значения
            y[i] = self.labels.index(y[i]) + 1
            number_of_labels[y[i] - 1] += 1
        self.attrs = [[] for _ in range(classes * 2 + 1)]  # таблица атрибутов
        # в этой таблице: массивы со словами, лейблы в цифрах, вероятностью того, что определённому слову будет выдан определённый лейбл
        self.predict_labels = [math.log(number / sum(number_of_labels)) for number in
                               number_of_labels]  # считаем возможную вероятность по теореме Байеса
        for i in range(len(x)):  # вычленяем слова из заголовков и добавляем их в массив
            words = split_row(x[i])
            for word in words:  # вычисляем для каждого слова сколько раз оно встречается (если пока не встречалось, добавляем его в массив)
                if word in self.attrs[0]:
                    self.attrs[y[i]][self.attrs[0].index(word)] += 1
                else:
                    self.attrs[0].append(word)
                    self.attrs[y[i]].append(1)
                    num_of_label = y[i]
                    for j in range(classes - 1):  # распределяем слова по лейблам (ставим им соответствующие цифры)
                        num_of_label = (num_of_label % classes) + 1
                        self.attrs[num_of_label].append(0)
                    for col in range(classes + 1, classes * 2 + 1):
                        self.attrs[col].append(0)
        words_on_labels = [sum(self.attrs[i + 1]) for i in range(classes)]  # кол-во слов, имеющих определённый лейбл в виде ['good','maybe','never']

        for row in range(len(self.attrs[0])):  # считаем вероятность того, что новость, содержащая какое-то слово понравится или не понравится
            for col in range(classes + 1, classes * 2 + 1):
                self.attrs[col][row] = (self.attrs[col - classes][row] + self.alpha) / \
                                       (words_on_labels[col - classes - 1] + self.alpha *
                                        len(self.attrs[0]))

    def predict(self, x):
        """ Perform classification on an array of test vectors X. """
        labels = []
        classes = len(self.labels)
        for string in x:  # идём по строке заголовка
            string_labels = [i for i in self.predict_labels]  # записываем возможные лейблы
            words = split_row(string)  # разбиваем заголовки
            for word in words:  # пытаемся определить лейбл для новости
                if word in self.attrs[0]:
                    for i in range(classes):
                        string_labels[i] += math.log(self.attrs[i + classes + 1][self.attrs[0].index(word)])
            for i in range(classes):  # ищем максимально вероятный лейбл и его и прописываем
                if string_labels[i] == max(string_labels):
                    labels.append(self.labels[i])
                    break
        return labels

    def score(self, x_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = self.predict(x_test)
        count = 0
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                count += 1
        return count / len(y_test)
