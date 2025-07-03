import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

TOKEN = os.environ.get("TOKEN")

produk = {
    "8991002101234": {"nama": "Indomie Goreng", "harga": 3000},
    "8991002104567": {"nama": "Teh Botol", "harga": 5000},
    "8991002107890": {"nama": "Aqua 600ml", "harga": 4000}
}

keranjang = []

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🛍️ Selamat datang di Bot Kasir!\nGunakan perintah:\n/scan <barcode>\n/bayar <jumlah uang>")

def scan(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("❗ Contoh: /scan 8991002101234")
        return
    
    kode = context.args[0]
    if kode in produk:
        item = produk[kode]
        keranjang.append(item)
        update.message.reply_text(f"✅ {item['nama']} | Rp {item['harga']:,} ditambahkan.")
    else:
        update.message.reply_text("❌ Barcode tidak ditemukan dalam database.")

def bayar(update: Update, context: CallbackContext):
    if not keranjang:
        update.message.reply_text("🛒 Keranjang masih kosong.")
        return
    
    if len(context.args) == 0:
        update.message.reply_text("❗ Contoh: /bayar 50000")
        return

    total = sum(item['harga'] for item in keranjang)
    bayar = int(context.args[0])
    kembalian = bayar - total

    daftar = "\n".join([f"- {item['nama']} | Rp {item['harga']:,}" for item in keranjang])
    hasil = f"🧾 Transaksi:\n{daftar}\n\nTotal: Rp {total:,}\nBayar: Rp {bayar:,}\nKembalian: Rp {kembalian:,}"
    update.message.reply_text(hasil)
    keranjang.clear()

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("scan", scan))
    dp.add_handler(CommandHandler("bayar", bayar))

    print("🤖 Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
