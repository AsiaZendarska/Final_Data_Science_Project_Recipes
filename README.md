# Projekt końcowy: Klasyfikacja Przepisów Kulinarnych 

&nbsp;
## Opis projektu:

Celem projektu jest stworzenie modeli do klasyfikacji przepisów kulinarnych na trzy kategorie: śniadania, obiady i kolacje. Dane zostały zebrane z trzech różnych stron internetowych z przepisami: Kwestia Smaku, Przepisy.pl oraz Ania Starmach. Projekt obejmuje przetwarzanie danych, eksploracyjną analizę danych oraz budowę modeli klasyfikacyjnych przy użyciu różnych algorytmów, w tym głębokich sieci neuronowych.

## Kroki projektu:

Zbieranie danych: Dane zostały zebrane z trzech różnych stron internetowych przy użyciu bibliotek requests i BeautifulSoup. Zebrane dane obejmują tytuły przepisów, składniki, sposób przygotowania, ocenę, liczbę opinii oraz czas przygotowania.

Przetwarzanie danych (EDA): Dane zostały przetworzone w celu usunięcia niepotrzebnych znaków, standaryzacji jednostek miar oraz usunięcia stopwordów. Przeprowadzono również ekstrakcję ilości składników oraz lematyzację tekstu przy użyciu biblioteki spacy. Przeprowadzono analizę danych, w tym sprawdzenie brakujących wartości, rozkłady kategorii oraz analizę najczęściej występujących składników. Wygenerowano również chmurę słów dla składników.

Budowa modeli klasyfikacyjnych i ich ewaluacja: 

- Regresja logistyczna
- Support Vector Machine (SVM)
- Random Forest
- Gradient Boosting
- Modele głębokich sieci neuronowych (DNN) z użyciem warstw RNN i LSTM
  
Modele zostały ocenione przy użyciu metryk takich jak dokładność, precyzja, recall oraz f1-score. Przeprowadzono również grid search w celu optymalizacji hiperparametrów.

## Użyte technologie i biblioteki:

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Requests
- BeautifulSoup
- Scikit-learn
- TensorFlow/Keras
- SpaCy
- WordCloud

## Wyniki:

Udało się zebrać i zorganizować dużą ilość danych (2563 przepisy), które są podstawą do dalszej analizy. Następnie przeszliśmy do analizy danych, dzięki czemu możemy stwierdzić, że przepisy są równomiernie rozłożone między kategorie (śniadania, obiady, kolacje). Usunęliśmy stopwordsy i przeprowadziliśmy standaryzację jednostek, co poprawiło jakość danych tekstowych i było kluczowe dla dalszego modelowania.
Użycie grid search i cross-validation pozwoliło na stworzenie optymalnych modeli, które dobrze radzą sobie z danymi testowymi. Po wytrenowaniu modeli możemy stwierdzić, że najlepszym modelem okazały się modele regresji logistycznej i SVM, zaś modele Random Forest i Gradient Boosting miały tendencję do przetrenowania. Zastosowanie lematyzacji poprawiło jakość danych tekstowych, co przełożyło się na lepsze wyniki modeli klasyfikacyjnych. Spośród testowanych modeli sieci neuronowych, model_1 osiągnął najlepsze wyniki.

## Wnioski:

Projekt wykazał, że proste modele klasyfikacyjne, takie jak regresja logistyczna i SVM, mogą być bardzo skuteczne w zadaniu klasyfikacji przepisów kulinarnych na podstawie składników. Modele głębokich sieci neuronowych również pokazały swoją skuteczność, choć w niektórych przypadkach mogą mieć tendencję do przetrenowania.
Jednakże, modele miały trudności z klasyfikacją niektórych przepisów do odpowiednich kategorii.

## Współpraca:

Projekt ten został zrealizowany we współpracy z moim kolegą. Wspólnie pracowaliśmy nad zbieraniem danych, przetwarzaniem ich oraz budową modeli klasyfikacyjnych. Dzięki wspólnej pracy udało nam się osiągnąć satysfakcjonujące wyniki i zgłębić różne aspekty analizy danych oraz machine learningu.
