from tabulate import tabulate

# Global variable untuk menyimpan semua character
character_list = []
current_character = None
no_chara = 1
equipment_list = [
    {'Nama': 'Sword', 'ATK': 10, 'DEF': 0},
    {'Nama': 'Shield', 'ATK': 0, 'DEF': 5}
]
enemy_list = [
    {'Nama': 'Slime', 'ATK': 5, 'DEF': 2, 'HP': 20},
    {'Nama': 'Goblin', 'ATK': 8, 'DEF': 4, 'HP': 30},
    {'Nama': 'Wolf', 'ATK': 12, 'DEF': 6, 'HP': 40}
]

def unequip_item(character):
    if character['equipped_item']:
        item_name = character['equipped_item']
        item = next((eq for eq in equipment_list if eq['Nama'] == item_name), None)
        if item:
            character['ATK'] -= item['ATK']
            character['DEF'] -= item['DEF']
        character['equipped_item'] = None
        print(f"🔧 {item_name} telah di-unequip.")
    else:
        print("⚠️  Tidak ada item yang sedang digunakan.")


def equip_item(character, item):
    # Cek item yang sama
    if character['equipped_item'] == item['Nama']:
        print(f"⚠️  Kamu sudah menggunakan {item['Nama']}.")
        return

    # supaya ga double stat
    if character['equipped_item']:
        unequip_item(character)

    # Equip item baru
    character['ATK'] += item['ATK']
    character['DEF'] += item['DEF']
    character['equipped_item'] = item['Nama']
    print(f"✅ {item['Nama']} berhasil di-equip!")

def lihat_inventory():
    global current_character
    print("="*40)
    print("🎒 INVENTORY".center(40))
    print("="*40)
    print(tabulate(equipment_list, headers="keys", tablefmt="fancy_grid"))
    print(f"Item saat ini: {current_character['equipped_item'] if current_character['equipped_item'] else 'None'}")
    #strip ngapus spasi awal akhir
    pilih = input("Equip item? (ketik nama), 'u' untuk unequip, atau enter untuk batal: ").strip()
    if pilih.lower() == 'u':
        unequip_item(current_character)
    elif pilih:
        item = next((eq for eq in equipment_list if eq['Nama'].lower() == pilih.lower()), None)
        if item:
            equip_item(current_character, item)
        else:
            print("Item tidak ditemukan.")


def show_menu():
    print("="*40)
    print("💫 WELCOME TO ADVENTURE GAME 💫".center(40))
    print("="*40)
    print('1. Buat Character\n2. Pilih Character\n3. Hapus Character\n4. Keluar')
    print("="*40)

def buat_character():
    global no_chara
    nama = input("Masukkan nama character: ")
    character = {
        'No': no_chara,
        'Nama': nama,
        "Level": 1,
        'EXP': 0,
        'ATK': 10,
        'DEF': 5,
        'HP': 100,
        'equipped_item': None
    }
    character_list.append(character)
    no_chara+=1
    print(f"Character {nama} berhasil dibuat!\n")

def pilih_character():
    global current_character
    if not character_list:
        print('Anda belum memiliki character, silahkan buat character terlebih dahulu\n')
        return
    print(tabulate(character_list, headers="keys", tablefmt="fancy_grid"))
    while True:
        pilih = int(input("Pilih Nomor Character (0 = kembali): "))
        #next cek iterasi selanjutnya
        current_character = next((char for char in character_list if char['No'] == pilih), None)
        if current_character:
            print(f"Kamu memilih {current_character['Nama']}!\n")
            break
        elif pilih==0:
            break
        else:
            print("Nomor salah, silahkan input character yang ada")

def hapus_character():
    global current_character
    if not character_list:
        print('Anda belum memiliki character, silahkan buat character terlebih dahulu\n')
        return
    print(tabulate(character_list, headers="keys", tablefmt="fancy_grid"))
    while True:
        pilih = int(input("Pilih Nomor Character yang ingin dihapus(0 = kembali): "))
        #next cek iterasi selanjutnya
        delete_character = next((char for char in character_list if char['No'] == pilih), None)
        if delete_character:
            character_list.remove(delete_character)
            print(f"{delete_character['Nama']} berhasil dihapus!\n")
            # Reset current_character jika dihapus
            if current_character and current_character['No'] == delete_character['No']:
                current_character = None
            break
        elif pilih==0:
            break
        else:
            print("Nomor salah, character tidak ditemukan\n")

def status_character():
    print("="*40)
    print(f"⚔️  STATUS CHARACTER".center(40))
    print("="*40)
    display_character = {k:v for k,v in current_character.items() if k != 'No'}
    print(tabulate([display_character], headers="keys", tablefmt="fancy_grid"))

def gain_exp(amount):
    current_character['EXP'] += amount
    print(f"{current_character['Nama']} mendapat {amount} EXP! (Total EXP: {current_character['EXP']})")
    while current_character['EXP'] >= 50:
        current_character['EXP'] -= 50
        current_character['Level'] += 1
        current_character['ATK'] += 2
        current_character['DEF'] += 1
        current_character['HP'] += 10
        print(f"LEVEL UP! {current_character['Nama']} sekarang Level {current_character['Level']} (+2 ATK, +1 DEF, +10 HP)")

def battle():
    global current_character
    import random
    enemy = random.choice(enemy_list)
    enemy_hp = enemy['HP']
    char_hp = current_character['HP']

    print("="*40)
    print(f"⚔️  BATTLE START: {current_character['Nama']} vs {enemy['Nama']}")
    print("="*40)

    while enemy_hp > 0 and char_hp > 0:
        # Character nyerang
        damage_to_enemy = max(current_character['ATK'] - enemy['DEF'], 1)
        enemy_hp -= damage_to_enemy
        print(f"{current_character['Nama']} menyerang {enemy['Nama']} dan memberikan {damage_to_enemy} damage! (HP Musuh: {max(enemy_hp,0)})")
        if enemy_hp <= 0:
            print(f"{enemy['Nama']} kalah!")
            gain_exp(10)
            break

        # musuh nyerang
        damage_to_char = max(enemy['ATK'] - current_character['DEF'], 1)
        char_hp -= damage_to_char
        print(f"{enemy['Nama']} menyerang {current_character['Nama']} dan memberikan {damage_to_char} damage! (HP kamu: {max(char_hp,0)})")
        if char_hp <= 0:
            print(f"Kamu kalah melawan {enemy['Nama']}!")
            break

    print("Battle selesai. HP kembali pulih.\n")

def menu_chara():
    global current_character
    while True:
        status_character()
        print("="*40)
        print('1. Battle\n2. Lihat Inventory\n3. Kembali ke Menu Awal\n4. Keluar')
        print("="*40)
        menu = int(input("Pilih menu: "))
        match menu:
            case 1:
                battle()
            case 2:
                lihat_inventory()
            case 3:
                current_character = None
                break
            case 4:
                print("👋 Keluar dari game. Terima kasih!")
                exit()
            case _:
                print("Input tidak benar\n")

def main():
    while True:
        if not current_character:
            show_menu()
            menu = int(input('Pilih: '))
            match menu:
                case 1:
                    buat_character()
                case 2:
                    pilih_character()
                case 3:
                    hapus_character()
                case 4:
                    print("👋 Terima kasih sudah bermain!")
                    break
                case _:
                    print('Input tidak benar\n')
        else:
            menu_chara()

if __name__ == "__main__":
    main()
