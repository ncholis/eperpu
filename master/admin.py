from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Siswa, Buku, Peminjam

# Register your models here.

class PeminjamAdmin(admin.ModelAdmin):
    list_display = ['s_siswa', 's_buku', 'dibuat', 'batas_pengembalian']
    list_filter = ('buku__judul', 'siswa__nama', 'dibuat')

    def s_siswa(self, obj):
        pret = '<div>%s</div>' % obj.siswa.nama
        return format_html('{}', mark_safe(pret))
    s_siswa.short_description = 'Nama'

    def s_buku(self, obj):
        pret = '<div>%s</div> ' % obj.buku.judul
        return format_html('{}', mark_safe(pret))
    s_buku.short_description = 'Buku'

admin.site.register(Siswa)
admin.site.register(Buku)
admin.site.register(Peminjam, PeminjamAdmin)
