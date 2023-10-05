def pad():
    x = {}
    for i in range(100):
        x["Pad_"+str(i)] = "NaN"
    return(x)

if __name__ == "__main__":
    pad()


padded=pad()

print(padded)
