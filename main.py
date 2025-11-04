"""

Классы бойцов:
- Tank (танк): много здоровья, низкая точность
- Medic (медик): лечится иногда вместо выстрела
- Damage (урон): высокий урон, меньше здоровья
- Sniper (меткий): высокая точность

Механика:
- Каждый ход атакующий пытается выстрелить — шанс попадания зависит от точности.
- Если попал — наносится урон. Медик иногда предпочитает лечиться сам.

"""

import random
import time
from typing import Tuple


class Fighter:
	def __init__(self, name: str, hp: int, damage: int, acc: float, role: str):
		self.name = name
		self.max_hp = hp
		self.hp = hp
		self.damage = damage
		self.acc = acc
		self.role = role

	def is_alive(self) -> bool:
		return self.hp > 0

	def dmg(self, amount: int):
		self.hp -= amount
		if self.hp < 0:
			self.hp = 0

	def heal(self, amount: int):
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def atack(self, target) -> Tuple[bool, int]: # Атака
		roll = random.random()
		if roll <= self.acc:
			target.dmg(self.damage)
			return True, self.damage
		else:
			return False, 0

	def __str__(self):
		return f"{self.name}({self.role}) HP:{self.hp}/{self.max_hp}"


class Tank(Fighter):
	def __init__(self, name="Tank"):
		super().__init__(name=name, hp=140, damage=14, acc=0.45, role="Tank")


class Medic(Fighter):
	def __init__(self, name="Medic"):
		super().__init__(name=name, hp=90, damage=10, acc=0.55, role="Medic")
		self.heal_amount = 18
		self.heal_chance = 0.30 

	def take_turn(self, target): # Лечение
		if random.random() < self.heal_chance and self.hp < self.max_hp:
			self.heal(self.heal_amount)
			return "heal", self.heal_amount
		else:
			hit, dmg = self.atack(target)
			return ("hit", dmg) if hit else ("miss", 0)


class Damage(Fighter):
	def __init__(self, name="Damage"):
		super().__init__(name=name, hp=75, damage=18, acc=0.55, role="Damage")


class Sniper(Fighter):
	def __init__(self, name="Sniper"):
		super().__init__(name=name, hp=80, damage=15, acc=0.78, role="Sniper")


def duel(f1: Fighter, f2: Fighter, verbose: bool = True, pause: float = 0.2): # Дуэль
	att, df = (f1, f2) if random.random() < 0.5 else (f2, f1)
	if verbose:
		print("=== Дуэль начинается ===")
		print(f"Бойцы: 1) {f1}  2) {f2}\n")

	while att.is_alive() and df.is_alive():
		if verbose:
			print(f"{att.name} ходит -> {df.name}")

		if isinstance(att, Medic):
			action, val = att.take_turn(df)
			if action == "heal":
				if verbose:
					print(f"{att.name} лечится на {val} HP. Сейчас: {att.hp}/{att.max_hp}")
			elif action == "hit":
				if verbose:
					print(f"{att.name} попал и нанёс {val} урона. {df.name} HP: {df.hp}/{df.max_hp}")
			else:
				if verbose:
					print(f"{att.name} промахнулся.")
		else:
			hit, dmg = att.atack(df)
			if hit:
				if verbose:
					print(f"{att.name} попал и нанёс {dmg} урона. {df.name} HP: {df.hp}/{df.max_hp}")
			else:
				if verbose:
					print(f"{att.name} промахнулся.")

		if not df.is_alive():
			if verbose:
				print(f"\n{df.name} пал. Победил {att.name}!")
			return att

		att, df = df, att
	
		if pause and verbose:
			time.sleep(pause)

	winner = f1 if f1.is_alive() else f2
	if verbose:
		print(f"\nПобедитель: {winner.name}")
	return winner


def demo():
	roster = [Tank("Tank = Islam"), Medic("Medic = Alina"), Damage("Damage = Abdu"), Sniper("Sniper = Nurbol")]
	f1, f2 = random.sample(roster, 2)
	winner = duel(f1, f2, verbose=True, pause=0.15)
	print('\n=== Результат дуэли ===')
	print(f"{f1}\n{f2}\nПобедил: {winner.name}")


if __name__ == '__main__': 
	demo()
