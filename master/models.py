from django.db import models
from django.core.exceptions import ValidationError
from django.db import connection

# Create your models here.

class Siswa(models.Model):
    nama = models.CharField('Nama', max_length=100)
    kelas = models.CharField('Kelas', max_length=20)
    tempat_lahir = models.CharField('Tempat lahir', max_length=50)
    tanggal_lahir = models.DateField('Tanggal lahir')

    def __str__(self):
        return self.nama


class Buku(models.Model):
    judul = models.CharField('Judul', max_length=200)
    deskripsi = models.TextField('Deskripsi', null=True, blank=True)
    stok = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.judul


class Peminjam(models.Model):
    siswa = models.ForeignKey(
        'Siswa', on_delete=models.CASCADE, related_name='bukupinjam')
    buku = models.ForeignKey(
        'Buku', on_delete=models.CASCADE, verbose_name='Buku yang dipinjam', related_name='pinjambuku')
    dibuat = models.DateField(auto_now_add=True, verbose_name='Dibuat')
    batas_pengembalian = models.DateField(verbose_name='Batas Pengembalian')
    _already_clean = False

    def __str__(self):
        return self.siswa.nama

    def print_query(self, qs):
        print(qs.query)

    def clean_stok(self):
        qs = self.buku.pinjambuku.filter(buku=self.buku).exclude(id=self.id)
        self.print_query(qs)

        bp = qs.count()
        if not bp:
            return

        if bp >= self.buku.stok:
            raise ValidationError('Buku Tidak Tersedia')

    def clean_batas_pengembalian(self):
        if not self.dibuat:
            return

        if self.dibuat > self.batas_pengembalian:
            raise ValidationError('Waktu pengembalian buku harus lebih dari waktu dibuat')

    def clean(self):
        self.clean_batas_pengembalian()
        self.clean_stok()
        self._already_clean =True

    def save(self, *args, **kwargs):
        if not self._already_clean:
            self.clean()

        self._already_clean = False
        return super(Peminjam, self).save(*args, **kwargs)
