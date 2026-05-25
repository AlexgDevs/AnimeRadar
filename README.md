# AnimeRadar Bot

**AnimeRadar** — асинхронный Telegram-бот для поиска и мониторинга аниме. Бот интегрируется с внешними API, парсит данные на лету и выводит результаты пользователю с использованием пагинации.

---

### 🛠 Стек технологий и инструменты

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/aiogram-3.x-26A69A?style=for-the-badge&logo=telegram&logoColor=white" alt="aiogram 3">
  <img src="https://img.shields.io/badge/aiohttp-Async--Client-2AA1DC?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDQgNnYxMmw4IDQgOC00VjZMMTIgMptGIDEyIDQuN0wxNy4zIDhsLTUuMyAzLTUuMy0zTDEyIDQuN002IDkuN2w1IDMuM3Y1LjNsLTUtMy4zVjkuN203IDguNnYtNS4zbDUtMy4zdjUuM2wtNSAzLjNaIi8+PC9zdmc+" alt="aiohttp">
</p>

* <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Search/SVG/ic_fluid_search_20_color.svg" width="18" height="18" align="center" /> **Интеграция с API:** Асинхронный парсинг внешних баз данных с помощью `aiohttp` без блокировки основного потока бота.
* <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Navigation/SVG/ic_fluid_navigation_20_color.svg" width="18" height="18" align="center" /> **Inline-пагинация:** Реализация удобного UI/UX для полистного просмотра результатов поиска через динамические инлайн-клавиатуры.
* <img src="https://raw.githubusercontent.com/microsoft/fluentui-system-icons/master/assets/Code/SVG/ic_fluid_code_20_color.svg" width="18" height="18" align="center" /> **Архитектура:** Модульная структура на роутерах (`aiogram 3`), разделяющая логику запросов к API и интерфейс взаимодействия с пользователем.
