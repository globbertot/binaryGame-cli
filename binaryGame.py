from random import choice
import readline # Fix arrow key navigation.
import argparse

class BinaryGame:
    def __init__(self, bits):
        """Initialize stats and settings"""
        self.score = 0;
        self.totalRounds = 0;
        self.solvedCount = 0;
        self.maxAttempts = 5;
        self.scoreLoss = 5;
        self.scoreWin = 5;

        self.bits = bits;

    def genBinary(self, length=8):
        """Generates a random binary number, with length being `length`"""
        binaryStr = ''.join(choice('01') for _ in range(length));
        decimal = int(binaryStr, 2);
        return {"binary": binaryStr, "decimal": decimal};

    def genHint(self, length=8):
        """Dynamically generates the powers of 2 as a hint"""
        return " | ".join(str(2**i) for i in range(length-1, -1, -1));

    def checkAnswer(self, attempt, gamemodeType, binaryDict):
        """Checks if `attempt` is the answer from `binaryDict` depending on the `gamemodeType`"""
        try:
            if gamemodeType == 0:  # Decimal to binary
                return int(attempt) == binaryDict["decimal"]
            elif gamemodeType == 1:  # Binary to decimal
                return attempt == binaryDict["binary"]
            else:
                return False
        except ValueError:
            print("Warning: Please only enter valid real numbers.")
            return False

    def playRound(self):
        """Round management"""
        binaryDict = self.genBinary(self.bits);
        gamemodeType = int(choice([0, 1])); 
        text = f"Find the decimal of `{binaryDict['binary']}`" if gamemodeType == 0 else f"Find the binary of `{binaryDict['decimal']}`";

        print(f"Gamemode: {gamemodeType}");
        print(f"Round {self.totalRounds}: {text}\n");
        attempts = self.maxAttempts;
        won = False;

        while (attempts > 0):
            hint = self.genHint(self.bits);
            print(f"Hint:\n {hint}");

            attempt = input("\nAnswer: ").strip();
            attempts -= 1;

            if (self.checkAnswer(attempt, gamemodeType, binaryDict)):
                print("Correct!");
                self.score += self.scoreWin;
                won = True;
                self.solvedCount += 1;
                break;
            else:
                print(f"Incorrect answer, Try harder!\nAttempts left: {attempts}/{self.maxAttempts}");

        if (not won):
            ans = binaryDict["binary"] if gamemodeType == 0 else binaryDict["decimal"];
            print(f"You lost score, The answer was: {ans}");
            self.score -= self.scoreLoss;
        print(f"Round over! Current Score: {self.score}");

    def play(self):
        """Game loop"""
        if self.bits > 64:
            print("Warning: The game may be EXTREMLY difficult with this many bits! Good luck!");

        while True:
            print("\n -- New round --");
            self.playRound();
            self.totalRounds += 1;

            c = input("Would you like to play again? (Y/n): ") or 'y';
            if (c.lower() != 'y'):
                break;

        print(f"Game End! | Final stats:\n"
              f"Rounds Played: {self.totalRounds}\n"
              f"Total Solved: {self.solvedCount}\n"
              f"Final Score: {self.score}\n");

parser = argparse.ArgumentParser(description="A simple binary guessing game from your terminal");
parser.add_argument('--bits', type=int, default=8, help="The number of bits to guess");

args = parser.parse_args();

game = BinaryGame(args.bits);
game.play();

