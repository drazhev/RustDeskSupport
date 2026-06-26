# RustDeskSupport

Лесен portable пакет за клиенти за отдалечена поддръжка чрез RustDesk.

## Как работи

Клиентът изтегля `rustdesk-drazhev.exe` от `support.drazhev.net`, стартира го и RustDesk се отваря предварително конфигуриран с частните сървъри.

## Сървърна конфигурация

- **ID/Relay сървър:** 192.168.222.21
- **API:** http://192.168.222.21:21114
- **Домейн за изтегляне:** support.drazhev.net

## Сборка

```bash
./scripts/build.sh
```

Резултатът е `build/rustdesk-drazhev.exe`.

## Структура

```
src/           - launcher скрипт и конфиг шаблон
assets/        - оригинален RustDesk portable .exe
build/         - генерирания файл за клиентите
docs/          - инструкция за клиента
scripts/       - скрипт за сборка
```
