from Model import Model

model = Model()

# testing
print model.preprocess([
    "The broader Standard & Poor's 500 Index <.SPX> shed 2.38 points, or 0.24 percent, at 995.10",
    "Albuquerque Mayor Martin Chavez said investigators felt confident that with the arrests they had \"at least one of the fires resolved.\""
])
print model.preprocess(["cater pillar", "caterpillar"])  # treba ispast [caterpillar] i [caterpillar]
print model.preprocess(["a b c de ef", "ab bc d e f"])  # treba ispast [ab c de ef] i [ab bc de f]
print model.preprocess(["$US1234 $US1,234.00 $US345.12 $US -123.13 a sada normalni broj = 213.12", ""])
print model.get_features(["r1", "r2"])
print model.get_features([["r1", "r2"], ["a", "b"]])
