import pandas as pd
import numpy as np

from chatbot import Chatbot

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================
# LOAD CHATBOT
# ==========================================

print("=" * 60)
print("MEMUAT CHATBOT")
print("=" * 60)

chatbot = Chatbot()

# ==========================================
# LOAD DATASET EVALUASI
# ==========================================

df = pd.read_csv(
    "evaluation_examples.csv"
)

print(f"\nJumlah Data Evaluasi : {len(df)}")

# ==========================================
# VARIABLE EVALUASI
# ==========================================

y_true = []
y_pred = []

results = []

# ==========================================
# PROSES EVALUASI
# ==========================================

print("\nMemulai Evaluasi...\n")

for index, row in df.iterrows():

    question = row["question"]
    true_intent = row["true_intent"]

    result = chatbot.reply(question)

    predicted_intent = result.get(
        "intent",
        "unknown"
    )

    correct = (
        true_intent == predicted_intent
    )

    y_true.append(true_intent)
    y_pred.append(predicted_intent)

    results.append({

        "question": question,

        "true_intent": true_intent,

        "predicted_intent": predicted_intent,

        "correct": correct

    })

    status = "✓" if correct else "✗"

    print(
        f"[{index+1:03d}] {status}"
    )

    print(
        f"Question : {question}"
    )

    print(
        f"True     : {true_intent}"
    )

    print(
        f"Predict  : {predicted_intent}"
    )

    print("-" * 60)

# ==========================================
# HITUNG METRICS
# ==========================================

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

correct_predictions = sum(
    np.array(y_true) == np.array(y_pred)
)

wrong_predictions = len(y_true) - correct_predictions

# ==========================================
# TAMPILKAN HASIL
# ==========================================

print("\n")
print("=" * 60)
print("HASIL EVALUASI CHATBOT")
print("=" * 60)

print(
    f"Total Pertanyaan     : {len(y_true)}"
)

print(
    f"Prediksi Benar       : {correct_predictions}"
)

print(
    f"Prediksi Salah       : {wrong_predictions}"
)

print(
    f"Accuracy             : {accuracy*100:.2f}%"
)

print(
    f"Precision            : {precision*100:.2f}%"
)

print(
    f"Recall               : {recall*100:.2f}%"
)

print(
    f"F1 Score             : {f1*100:.2f}%"
)

print("=" * 60)

# ==========================================
# SIMPAN HASIL KE CSV
# ==========================================

result_df = pd.DataFrame(results)

result_df.to_csv(

    "hasil_evaluasi.csv",

    index=False,

    encoding="utf-8-sig"

)

print(
    "\nHasil evaluasi disimpan ke hasil_evaluasi.csv"
)

# ==========================================
# CONFUSION MATRIX
# ==========================================

labels = sorted(
    list(
        set(y_true)
    )
)

cm = confusion_matrix(

    y_true,

    y_pred,

    labels=labels

)

# persentase per baris
cm_percent = (
    cm.astype("float")
    / cm.sum(axis=1)[:, np.newaxis]
) * 100

annotations = []

for i in range(cm.shape[0]):

    row = []

    for j in range(cm.shape[1]):

        row.append(

            f"{cm[i,j]}\n{cm_percent[i,j]:.1f}%"

        )

    annotations.append(row)

# ==========================================
# PLOT CONFUSION MATRIX
# ==========================================

plt.figure(
    figsize=(14, 10)
)

sns.heatmap(

    cm,

    annot=annotations,

    fmt="",

    cmap="Blues",

    linewidths=1,

    linecolor="gray",

    xticklabels=labels,

    yticklabels=labels,

    cbar=True

)

plt.title(

    "Confusion Matrix Evaluasi Chatbot Universitas Malikussaleh",

    fontsize=18,

    pad=20

)

plt.xlabel(

    "Intent Prediksi",

    fontsize=14

)

plt.ylabel(

    "Intent Aktual",

    fontsize=14

)

plt.xticks(

    rotation=45,

    ha="right"

)

plt.yticks(

    rotation=0

)

plt.tight_layout()

plt.savefig(

    "confusion_matrix.png",

    dpi=300,

    bbox_inches="tight"

)

plt.show()

print(
    "\nConfusion matrix berhasil disimpan sebagai confusion_matrix.png"
)

# ==========================================
# BAR CHART METRICS
# ==========================================

metrics = {

    "Accuracy": accuracy * 100,

    "Precision": precision * 100,

    "Recall": recall * 100,

    "F1-Score": f1 * 100

}

plt.figure(
    figsize=(8,6)
)

bars = plt.bar(

    metrics.keys(),

    metrics.values()

)

for bar in bars:

    height = bar.get_height()

    plt.text(

        bar.get_x() + bar.get_width()/2,

        height + 0.5,

        f"{height:.2f}%",

        ha='center'

    )

plt.ylim(0,100)

plt.ylabel(
    "Persentase (%)"
)

plt.title(
    "Performa Keseluruhan Chatbot"
)

plt.grid(
    axis='y',
    linestyle='--',
    alpha=0.5
)

plt.tight_layout()

plt.savefig(

    "evaluation_metrics.png",

    dpi=300,

    bbox_inches="tight"

)

plt.show()

print(
    "Grafik evaluasi berhasil disimpan sebagai evaluation_metrics.png"
)