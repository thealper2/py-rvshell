# py-rvshell

Python Reverse shell command and control

## Gereksinimler

py-rvshell aşağıdaki kütüphaneleri kullanır.

* Colorama
* Mss
* Requests
* Simplejson

## Kurulumu

Projeyi klonlamak için;

```python
git clone https://github.com/thealper2/py-rvshell.git
```
Gerekli kütüphaneleri kurmak için;

```python
python -m pip install -r requirements.txt
```

## Kullanımı
 
| Fonksiyon    | Kullanımı |
| ---------    | --------- |
| download     | Hedeften dosya indirmeye yarar. |
| upload       | Hedefe dosya yüklemeye yarar. |
| help         | Yardım tablosunu açmaya yarar. |
| get          | URL üzerinden dosya indirmeye yarar. |
| screenshot   | Ekran görüntüsü almaya yarar |
| post-exploit | Kalıcılığı sağlamaya yarar. |
| check        | İşletim sistemi türünü belirlemeye yarar. |

## Örnekler

```python
python3 server.py
python3 client.py
```
