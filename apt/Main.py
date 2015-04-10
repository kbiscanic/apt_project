from Model import Model

model = Model()

# testing
print(model.preprocess("The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10"))
print(model.preprocess(
    "Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""))
print(model.preprocess("Still, he said, \"I\'m absolutely confident we're going to have a bill.\""))