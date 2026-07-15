from chatbot import Chatbot

bot = Chatbot()

print("=" * 50)
print("        UNIMALBOT v1")
print("=" * 50)
print("Ketik 'exit' untuk keluar.\n")

while True:

    question = input("Anda : ")

    if question.lower() == "exit":

        print("\nTerima kasih telah menggunakan UNIMALBOT.")

        break

    result = bot.reply(question)

    print("Intent :", result["intent"])
    print("Score  :", result["score"])
    print("Bot    :", result["response"])
    print()