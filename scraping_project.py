from bs4 import BeautifulSoup
import requests
import random
from time import sleep

answers = []
quotes = []
hrefs = []


def hint_1(name, dictionary):
	'''Returns the first hint for the game logic.'''
	about_response = requests.get("http://quotes.toscrape.com" + dictionary[name])
	more_soup = BeautifulSoup(about_response.text, "html.parser")
	hint_bank_text = more_soup.find_all("span")
	date = hint_bank_text[0].get_text()
	place = hint_bank_text[1].get_text()
	return f"This person was born on {date} in {place}."

def hint_2(name):
	'''Returns the second hint for the game logic'''
	return f"This person's first name starts with the letter {name[0]}"

def hint_3(name):
	'''Returns the third hint for the game logic'''
	name_hint = name.split(" ")
	return f"This person's last name starts with the letter {name_hint[1][0]}"

def give_answer(name):
	'''Returns the answer to the game.'''
	return f"Sorry you didn't get it correct! The right answer is {name}."

def start_the_game():
	'''Creates the necessary answer bank and chooses a quote at random'''
	count = 1
	while True:
		response = requests.get("http://quotes.toscrape.com/page/" + f"{count}")
		soup = BeautifulSoup(response.text, "html.parser")
		main_text = soup.find_all("div", class_="quote")
		if main_text == []:
			break
		else:
			for answer in main_text:
				answers.append(answer.find("small").get_text())
			for saying in main_text:
				quotes.append(saying.find("span", class_="text").get_text())
			for link in main_text:
				a_tag = link.find("a")
				url = a_tag["href"]
				hrefs.append(url)	
			count += 1
			sleep(2)
	quote_bank = dict(zip(answers, quotes))
	about_pages = dict(zip(answers, hrefs))
	
	return quote_bank, about_pages

quotes, pages = start_the_game()
while True:
	answer = random.choice(answers)
	hint_text = pages
	quote = quotes[answer]
	guess_1 = input(f"Who said the following quote? - {quote} ")
	if guess_1.lower() == answer.lower():
		print("Congratulations! You are correct!")
	else:
		print("Sorry, that is incorrect. Here's a hint!")
		print(hint_1(answer, hint_text))
		guess_2 = input("Who is it? ")
		if guess_2.lower() == answer.lower():
			print("Congratulations! You are correct!")
		else:
			print("Sorry, that is incorrect. Here's another hint!")
			print(hint_2(answer))
			guess_3 = input("Who is it? ")
			if guess_3.lower() == answer.lower():
				print("Congratulations! Glad you were able to figure it out!")
			else:
				print(hint_3(answer))
				final_guess = input("Last chance! Who do you think it is? ")
				if final_guess.lower() == answer.lower():
					print("Whew! That was a close one!")
				else:
					print(give_answer(answer))
	keep_playing = input("Would you like to play again? y/n: ")
	if keep_playing == "y":
		pass
	else:
		break

