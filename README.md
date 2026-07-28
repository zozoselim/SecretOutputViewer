# Secret Output Viewer

Secret Output Viewer, Environment Secrets Store tarafından gönderilen environment variable referanslarını alır ve aynı NovaVision runtime ortamında bu değişkenlerin gerçek değerlerini çözer.

Gerçek secret değerleri yalnızca component belleğinde tutulur. Output olarak yalnızca güvenli bir başarı mesajı döndürülür.

## Kullanım

Bağlantı:

```text
Environment Secrets Store.secretReferences
    → Secret Output Viewer.secretReferences
```

Örnek giriş:

```json
["DOCKER_NETWORK"]
```

Başarılı çıktı:

```text
1 secret reference(s) were resolved and consumed successfully.
Secret values are masked.
```

## Geliştirme

```bash
python -m pytest -q
```

Bu paket test amaçlı bir downstream consumer olarak geliştirilmiştir ve secret değerlerini ekrana veya workflow outputuna yazmaz.
