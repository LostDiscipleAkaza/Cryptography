text = input("Enter message: ")
rails = int(input("Enter number of rails: "))

fence = [""] * rails
rail = 0
direction = 1

for ch in text:
    fence[rail] += ch

    if rail == 0:
        direction = 1
    elif rail == rails - 1:
        direction = -1

    rail += direction

print("Encrypted:", "".join(fence))