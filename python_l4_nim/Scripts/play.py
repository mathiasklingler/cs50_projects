from nim import train, play

ai = train(10000)
# print("self.q: ")
# for key, value in ai.q.items():
    # print(key, value)
play(ai)
