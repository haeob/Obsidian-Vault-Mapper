import sys
import os
import json
import subprocess
import urllib.parse
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QLabel,
                               QFrame, QScrollArea, QMenu, QInputDialog,
                               QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QDesktopServices, QCursor, QIcon, QPixmap, QPainter

APP_VERSION = "1.0"
GITHUB_AUTHOR = "https://github.com/haeob"
GITHUB_REPO = "https://github.com/haeob/Obsidian-Vault-Mapper"

# --- 1. 优化后的翻译字典 ---
I18N = {
    "en": {
        "title": "Obsidian Vault Mapper", "search": "🔍 Search vaults...", "new_cat": "+ New", "lang": "🌐 Lang",
        "categories": "Categories", "pinned": "Pinned", "unclassified": "Unclass.", "open": "Open",
        "new_cat_dialog": "New Category", "input_name": "Name:", "reveal": "📂 Reveal",
        "pin": "📌 Pin", "unpin": "📍 Unpin", "export": "📤 Export",
        "refresh": "🔄 Refresh", "refreshing": "⏳ Refreshing...", "total": "Total",
        "rename": "✏️ Rename", "delete": "🗑️ Delete", "export_done": "Exported successfully!",
        "export_title": "Export", "err_config": "⚠️ obsidian.json not found!", "err_read": "⚠️ Read error",
        "about": "ℹ️ About", "author_info": "Author Info", "version": "Version", "license": "License",
        "thanks": "Thanks to PySide6", "about_title": "About", "about_text": "Obsidian Vault Mapper\nVersion 1.0\nMIT License\nAuthor: haeob\nGitHub: https://github.com/haeob\nRepo: https://github.com/haeob/Obsidian-Vault-Mapper\nThanks to PySide6",
        "github_author": "Open Author GitHub", "github_repo": "Open Repository"
    },
    "zh": {
        "title": "Obsidian Vault 映射器", "search": "🔍 搜索仓库...", "new_cat": "+ 新建", "lang": "🌐 语言",
        "categories": "分类", "pinned": "置顶", "unclassified": "未分类", "open": "打开",
        "new_cat_dialog": "新分类", "input_name": "名称:", "reveal": "📂 打开",
        "pin": "📌 置顶", "unpin": "📍 取消置顶", "export": "📤 导出",
        "refresh": "🔄 刷新", "refreshing": "⏳ 正在刷新...", "total": "总数",
        "rename": "✏️ 重命名", "delete": "🗑️ 删除", "export_done": "导出成功！",
        "export_title": "导出", "err_config": "⚠️ 未找到 Obsidian 配置文件", "err_read": "⚠️ 配置文件读取失败",
        "about": "ℹ️ 关于", "author_info": "作者信息", "version": "版本", "license": "许可",
        "thanks": "感谢 PySide6", "about_title": "关于", "about_text": "Obsidian Vault Mapper\n版本 1.0\nMIT 许可证\n作者: haeob\nGitHub: https://github.com/haeob\n仓库: https://github.com/haeob/Obsidian-Vault-Mapper\n感谢 PySide6",
        "github_author": "打开作者 GitHub", "github_repo": "打开仓库"
    },
    "ja": {
        "title": "Obsidian Vault Mapper", "search": "🔍 ボールトを検索...", "new_cat": "+ 新規", "lang": "🌐 言語",
        "categories": "カテゴリ", "pinned": "ピン留め", "unclassified": "未分類", "open": "開く",
        "new_cat_dialog": "新規カテゴリ", "input_name": "名前:", "reveal": "📂 表示",
        "pin": "📌 ピン留め", "unpin": "📍 解除", "export": "📤 エクスポート",
        "refresh": "🔄 更新", "refreshing": "⏳ 更新中...", "total": "合計",
        "rename": "✏️ 名前変更", "delete": "🗑️ 削除", "export_done": "エクスポート完了！",
        "export_title": "エクスポート", "err_config": "⚠️ obsidian.jsonが見つかりません", "err_read": "⚠️ 読み込みエラー",
        "about": "ℹ️ 情報", "author_info": "作者情報", "version": "バージョン", "license": "ライセンス",
        "thanks": "PySide6に感謝", "about_title": "情報", "about_text": "Obsidian Vault Mapper\nバージョン 1.0\nMITライセンス\n作者: haeob\nGitHub: https://github.com/haeob\nリポジトリ: https://github.com/haeob/Obsidian-Vault-Mapper\nPySide6に感謝",
        "github_author": "作者 GitHub を開く", "github_repo": "リポジトリを開く"
    },
    "ru": {
        "title": "Obsidian Vault Mapper", "search": "🔍 Поиск хранилищ...", "new_cat": "+ Новый", "lang": "🌐 Язык",
        "categories": "Категории", "pinned": "Закреплено", "unclassified": "Без категории", "open": "Открыть",
        "new_cat_dialog": "Новая категория", "input_name": "Имя:", "reveal": "📂 Показать",
        "pin": "📌 Закрепить", "unpin": "📍 Открепить", "export": "📤 Экспорт",
        "refresh": "🔄 Обновить", "refreshing": "⏳ Обновление...", "total": "Всего",
        "rename": "✏️ Переименовать", "delete": "🗑️ Удалить", "export_done": "Экспорт успешно завершен!",
        "export_title": "Экспорт", "err_config": "⚠️ obsidian.json не найден!", "err_read": "⚠️ Ошибка чтения",
        "about": "ℹ️ О программе", "author_info": "Инфо об авторе", "version": "Версия", "license": "Лицензия",
        "thanks": "Спасибо PySide6", "about_title": "О программе", "about_text": "Obsidian Vault Mapper\nВерсия 1.0\nЛицензия MIT\nАвтор: haeob\nGitHub: https://github.com/haeob\nРепозиторий: https://github.com/haeob/Obsidian-Vault-Mapper\nСпасибо PySide6",
        "github_author": "Открыть автора GitHub", "github_repo": "Открыть репозиторий"
    }
}

# --- 2. 优化后的滚动条 (加宽感应区) ---
SCROLL_STYLE = """
QScrollBar:vertical {
    background: transparent;
    width: 18px; /* 更易点击 */
    margin: 2px 4px 2px 4px;
}
QScrollBar:horizontal {
    background: transparent;
    height: 18px;
    margin: 4px 2px 4px 2px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: rgba(48, 54, 61, 180);
    min-height: 56px;
    min-width: 56px;
    border-radius: 9px;
    border: 2px solid rgba(255,255,255,0.04);
    background-clip: content;
}
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
    background: rgba(88, 166, 255, 195);
}
QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {
    background: rgba(88, 166, 255, 255);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { height: 0px; width: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
"""


# --- 3. 数据管理 ---
class VaultManager:
    def __init__(self):
        self.path = Path("vault_master.json")
        self.error_msg = ""
        self.data = {"categories": [], "vaults": [], "settings": {"lang": "zh"}}
        self.load()

    def load(self):
        self.data.setdefault("categories", [])
        self.data.setdefault("vaults", [])
        self.data.setdefault("settings", {"lang": "zh"})
        if self.path.exists():
            try:
                with self.path.open('r', encoding='utf-8') as f:
                    self.data.update(json.load(f))
            except (OSError, json.JSONDecodeError):
                self.error_msg = "err_read"
        self.sync_obsidian()

    def sync_obsidian(self):
        self.error_msg = ""
        ob_path = Path(os.getenv('APPDATA', '')) / 'obsidian' / 'obsidian.json'
        if not ob_path.exists():
            self.error_msg = "err_config"
            return

        try:
            with ob_path.open('r', encoding='utf-8') as f:
                v_dict = json.load(f).get("vaults", {})
                ob_paths = {v['path'] for v in v_dict.values() if isinstance(v.get('path'), str)}
                # 过滤失效路径
                self.data['vaults'] = [v for v in self.data['vaults'] if v['path'] in ob_paths]
                # 增量更新
                existing_paths = {v['path'] for v in self.data['vaults']}
                for path in sorted(ob_paths):
                    if path not in existing_paths:
                        self.data['vaults'].append({
                            "path": path,
                            "name": os.path.basename(path),
                            "category": "Unclassified",
                            "pinned": False
                        })
        except (OSError, json.JSONDecodeError):
            self.error_msg = "err_read"
        self.save()

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)


# --- 4. 核心 UI 组件 ---
class VaultCard(QFrame):
    def __init__(self, info, mgr, refresh_cb, add_cat_cb, move_vault_cb):
        super().__init__()
        self.info, self.mgr, self.refresh = info, mgr, refresh_cb
        self.add_cat_ui, self.move_vault = add_cat_cb, move_vault_cb
        self.t = I18N[self.mgr.data['settings']['lang']]
        self.init_ui()

    def init_ui(self):
        self.setObjectName("VaultCard")
        self.setFixedHeight(75)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_more_menu)
        self.setStyleSheet(
            "#VaultCard{background:#161b22; border:1px solid #30363d; border-radius:12px;} #VaultCard:hover{border-color:#58a6ff; background:#1c2128;}")

        lay = QHBoxLayout(self);
        lay.setContentsMargins(15, 0, 15, 0)
        txt = QVBoxLayout();
        txt.setSpacing(1)
        is_p = self.info.get('pinned')
        name = QLabel(f"{'★ ' if is_p else ''}{self.info['name']}")
        name.setStyleSheet(f"font-weight:bold; color:{'#f1e05a' if is_p else '#f0f6fc'}; font-size:14px;")
        path = QLabel(self.info['path']);
        path.setStyleSheet("font-size:10px; color:#484f58;")
        txt.addWidget(name);
        txt.addWidget(path);
        lay.addLayout(txt, 2)

        btns = QHBoxLayout();
        btns.setSpacing(6)
        for d, sym in [(-1, "↑"), (1, "↓")]:
            b = QPushButton(sym);
            b.setFixedSize(26, 26)
            b.setStyleSheet("background:#21262d; color:#8b949e; border:none; border-radius:6px;")
            b.clicked.connect(lambda chk=False, delta=d: self.move_vault(self.info, delta))
            btns.addWidget(b)

        op = QPushButton(self.t["open"]);
        op.setFixedSize(75, 28)
        op.setStyleSheet("background:#238636; color:white; font-weight:bold; border-radius:14px; font-size:10px;")
        op.clicked.connect(self.do_open);
        btns.addWidget(op)

        disp_c = self.info['category'] if self.info['category'] != "Unclassified" else self.t["unclassified"]
        cat = QPushButton(disp_c)
        cat.setFixedSize(100, 28);
        cat.setStyleSheet(
            "background:transparent; border:1px solid #30363d; color:#8b949e; border-radius:14px; font-size:10px;")
        cat.clicked.connect(self.show_cat_menu);
        btns.addWidget(cat)
        lay.addLayout(btns)

    def do_open(self):
        url = f"obsidian://open?vault={urllib.parse.quote(os.path.basename(self.info['path']))}"
        QDesktopServices.openUrl(QUrl(url))

    def mouseDoubleClickEvent(self, event):
        self.do_open()

    def show_cat_menu(self):
        m = QMenu(self);
        m.setStyleSheet("QMenu{background:#161b22; color:white; border:1px solid #30363d;}")
        for c in self.mgr.data['categories'] + [self.t["unclassified"]]:
            m.addAction(c, lambda n=c: self.set_cat(n))
        m.addSeparator()
        m.addAction(self.t["new_cat"] + "...", self.create_and_assign)
        m.exec(QCursor.pos())

    def create_and_assign(self):
        n = self.add_cat_ui()
        if n: self.set_cat(n)

    def set_cat(self, c):
        self.info['category'] = "Unclassified" if c == self.t["unclassified"] else c
        self.mgr.save();
        self.refresh()

    def show_more_menu(self):
        m = QMenu(self);
        m.setStyleSheet("QMenu{background:#161b22; color:white; border:1px solid #30363d;}")
        m.addAction(self.t["reveal"], lambda: subprocess.run(['explorer', os.path.normpath(self.info['path'])]))
        pin_txt = self.t["unpin"] if self.info.get('pinned') else self.t["pin"]
        m.addAction(pin_txt, self.toggle_pin);
        m.exec(QCursor.pos())

    def toggle_pin(self):
        self.info['pinned'] = not self.info.get('pinned', False);
        self.mgr.save();
        self.refresh()


# --- 5. 主窗口 ---
class ObsidianManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mgr = VaultManager()
        self.category_widgets = {}
        self.init_ui()

    def init_ui(self):
        self.t = I18N[self.mgr.data['settings']['lang']]
        self.setWindowTitle("obvm")
        self.resize(1150, 850)

        pix = QPixmap(32, 32);
        pix.fill(Qt.transparent)
        ptr = QPainter(pix);
        ptr.drawText(pix.rect(), Qt.AlignCenter, "🥰");
        ptr.end()
        self.setWindowIcon(QIcon(pix))
        self.setStyleSheet(f"QMainWindow{{background:#0d1117;}} {SCROLL_STYLE}")

        central = QWidget();
        self.setCentralWidget(central)
        main_lay = QHBoxLayout(central);
        main_lay.setContentsMargins(0, 0, 0, 0);
        main_lay.setSpacing(0)

        # 侧边栏
        side = QFrame();
        side.setFixedWidth(250);
        side.setStyleSheet("background:#010409; border-right:1px solid #30363d;")
        self.side_lay = QVBoxLayout(side);
        self.side_lay.setContentsMargins(15, 30, 15, 15)
        self.cat_header = QLabel(self.t["categories"].upper(), styleSheet="color:#484f58; font-weight:bold; font-size:10px; margin-left:10px;")
        self.side_lay.addWidget(self.cat_header)

        self.cat_scroll = QScrollArea();
        self.cat_scroll.setWidgetResizable(True);
        self.cat_scroll.setStyleSheet("background:transparent; border:none;")
        self.cat_cont = QWidget();
        self.cat_vbox = QVBoxLayout(self.cat_cont);
        self.cat_vbox.setSpacing(8);
        self.cat_vbox.setAlignment(Qt.AlignTop)
        self.cat_scroll.setWidget(self.cat_cont);
        self.side_lay.addWidget(self.cat_scroll)

        bot_btns = QVBoxLayout();
        bot_btns.setSpacing(8)
        self.btn_export = QPushButton(self.t["export"])
        self.btn_export.setStyleSheet("background:#21262d; color:white; border-radius:8px; padding:10px;")
        self.btn_export.clicked.connect(self.export_md);
        bot_btns.addWidget(self.btn_export)

        btn_add = QPushButton(self.t["new_cat"])
        btn_add.setStyleSheet("background:#238636; color:white; border-radius:8px; padding:12px; font-weight:bold;")
        btn_add.clicked.connect(self.add_cat_dialog);
        bot_btns.addWidget(btn_add)

        self.btn_lang = QPushButton(self.t["lang"])
        self.btn_lang.setStyleSheet(
            "background:#21262d; color:#8b949e; border:1px solid #30363d; border-radius:8px; padding:8px;")
        self.btn_lang.clicked.connect(self.show_lang_menu);
        bot_btns.addWidget(self.btn_lang)

        self.btn_about = QPushButton(self.t["about"])
        self.btn_about.setStyleSheet(
            "background:#21262d; color:#8b949e; border:1px solid #30363d; border-radius:8px; padding:8px;")
        self.btn_about.clicked.connect(self.show_about);
        bot_btns.addWidget(self.btn_about)

        self.version_label = QLabel(f"{self.t['version']}: {APP_VERSION}    {self.t['license']}: MIT")
        self.version_label.setStyleSheet("color:#8b949e; font-size:11px; margin-top:10px;")
        self.version_label.setAlignment(Qt.AlignCenter)
        bot_btns.addWidget(self.version_label)

        self.side_lay.addLayout(bot_btns)
        main_lay.addWidget(side)

        # 主内容区
        content = QWidget();
        c_lay = QHBoxLayout(content);
        c_lay.addStretch(1)
        core = QWidget();
        core.setFixedWidth(880);
        core_lay = QVBoxLayout(core);
        core_lay.setContentsMargins(0, 30, 0, 0)

        self.search = QLineEdit();
        self.search.setPlaceholderText(self.t["search"])
        self.search.setStyleSheet(
            "background:#010409; border:1px solid #30363d; border-radius:12px; padding:12px 18px; color:white;")
        self.search.textChanged.connect(self.refresh_list);
        core_lay.addWidget(self.search)

        self.main_scroll = QScrollArea();
        self.main_scroll.setWidgetResizable(True);
        self.main_scroll.setStyleSheet("background:transparent; border:none;")
        self.list_cont = QWidget();
        self.list_lay = QVBoxLayout(self.list_cont);
        self.list_lay.setAlignment(Qt.AlignTop);
        self.list_lay.setSpacing(12)
        self.main_scroll.setWidget(self.list_cont);
        core_lay.addWidget(self.main_scroll)

        stat_lay = QHBoxLayout();
        stat_lay.setContentsMargins(10, 10, 10, 10)
        self.stat_label = QLabel("");
        self.stat_label.setStyleSheet("color:#484f58; font-size:11px;")
        self.btn_ref = QPushButton(self.t["refresh"])
        self.btn_ref.setFixedSize(110, 26);
        self.btn_ref.setStyleSheet("background:#21262d; color:#8b949e; border-radius:6px; font-size:10px;")
        self.btn_ref.clicked.connect(self.handle_refresh)
        stat_lay.addWidget(self.stat_label);
        stat_lay.addStretch();
        stat_lay.addWidget(self.btn_ref)
        core_lay.addLayout(stat_lay)

        c_lay.addWidget(core, 0);
        c_lay.addStretch(1)
        main_lay.addWidget(content, 1)
        self.refresh_list()

    def handle_refresh(self):
        self.btn_ref.setText(self.t["refreshing"]);
        self.btn_ref.setEnabled(False)
        self.mgr.sync_obsidian()
        QTimer.singleShot(600, self.finish_refresh)

    def finish_refresh(self):
        self.refresh_list();
        self.btn_ref.setText(self.t["refresh"]);
        self.btn_ref.setEnabled(True)

    def refresh_list(self):
        self.category_widgets = {}
        if self.mgr.error_msg:
            self.stat_label.setText(self.t[self.mgr.error_msg])
            self.stat_label.setStyleSheet("color:#f85149; font-weight:bold;")
        else:
            self.stat_label.setText(f"{self.t['total']}: {len(self.mgr.data['vaults'])}")
            self.stat_label.setStyleSheet("color:#484f58;")

        while self.cat_vbox.count(): self.cat_vbox.takeAt(0).widget().deleteLater()
        all_cats = self.mgr.data['categories'] + [self.t["unclassified"]]
        for c in all_cats:
            row = QWidget();
            r_lay = QHBoxLayout(row);
            r_lay.setContentsMargins(0, 0, 0, 0);
            r_lay.setSpacing(4)
            btn = QPushButton(c);
            btn.setMinimumHeight(38);
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(
                "QPushButton{background:#161b22; color:#8b949e; border:1px solid #30363d; border-radius:8px; text-align:left; padding-left:12px;} QPushButton:hover{color:#58a6ff; border-color:#58a6ff;}")
            btn.clicked.connect(lambda chk=False, n=c: self.scroll_to_cat(n))
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, n=c: self.show_cat_menu(n))
            r_lay.addWidget(btn, 1)

            if c != self.t["unclassified"]:
                for d, sym in [(-1, "↑"), (1, "↓")]:
                    sb = QPushButton(sym);
                    sb.setFixedSize(22, 38);
                    sb.setStyleSheet("background:#0d1117; color:#30363d; border:1px solid #21262d; border-radius:4px;")
                    sb.clicked.connect(lambda chk=False, n=c, delta=d: self.move_cat(n, delta))
                    r_lay.addWidget(sb)
            self.cat_vbox.addWidget(row)

        while self.list_lay.count():
            w = self.list_lay.takeAt(0).widget()
            if w: w.deleteLater()

        q = self.search.text().lower()
        all_v = [v for v in self.mgr.data['vaults'] if q in v['name'].lower() or q in v['path'].lower()]

        pinned = [v for v in all_v if v.get('pinned')]
        if pinned:
            self.list_lay.addWidget(QLabel(self.t["pinned"],
                                           styleSheet="color:#f1e05a; font-weight:bold; font-size:10px; margin:10px 0 5px 10px;"))
            for v in pinned: self.list_lay.addWidget(
                VaultCard(v, self.mgr, self.refresh_list, self.add_cat_dialog, self.move_vault))
            line = QFrame();
            line.setFixedHeight(1);
            line.setStyleSheet("background:#30363d; margin:10px 0;");
            self.list_lay.addWidget(line)

        others = [v for v in all_v if not v.get('pinned')]
        cat_order = self.mgr.data['categories'] + ["Unclassified"]
        others.sort(key=lambda x: cat_order.index(x['category']) if x['category'] in cat_order else 999)

        last_c = ""
        for v in others:
            disp_c = self.t["unclassified"] if v['category'] == "Unclassified" else v['category']
            if disp_c != last_c:
                header = QWidget();
                h_lay = QHBoxLayout(header);
                h_lay.setContentsMargins(10, 20, 10, 5)
                h_lbl = QLabel(disp_c.upper(), styleSheet="color:#484f58; font-weight:bold; font-size:10px;")
                h_lay.addWidget(h_lbl, 1)
                if v['category'] != "Unclassified":
                    for d, sym in [(-1, "↑"), (1, "↓")]:
                        b = QPushButton(sym);
                        b.setFixedSize(22, 20);
                        b.setStyleSheet(
                            "background:transparent; color:#30363d; border:1px solid #21262d; border-radius:4px;")
                        b.clicked.connect(lambda chk=False, n=v['category'], delta=d: self.move_cat(n, delta))
                        h_lay.addWidget(b)
                self.list_lay.addWidget(header)
                self.category_widgets[disp_c] = header
                last_c = disp_c
            self.list_lay.addWidget(VaultCard(v, self.mgr, self.refresh_list, self.add_cat_dialog, self.move_vault))

    def scroll_to_cat(self, name):
        if name in self.category_widgets:
            self.main_scroll.verticalScrollBar().setValue(self.category_widgets[name].pos().y())

    def move_cat(self, name, delta):
        c_list = self.mgr.data['categories']
        if name in c_list:
            i = c_list.index(name);
            ni = i + delta
            if 0 <= ni < len(c_list):
                c_list[i], c_list[ni] = c_list[ni], c_list[i]
                self.mgr.save();
                self.refresh_list()

    def move_vault(self, v, delta):
        vs = self.mgr.data['vaults']
        cvs = [x for x in vs if x['category'] == v['category']]
        i = cvs.index(v);
        ni = i + delta
        if 0 <= ni < len(cvs):
            gi, gni = vs.index(v), vs.index(cvs[ni])
            vs[gi], vs[gni] = vs[gni], vs[gi]
            self.mgr.save();
            self.refresh_list()

    def show_cat_menu(self, name):
        if name == self.t["unclassified"]: return
        m = QMenu(self);
        m.setStyleSheet("QMenu{background:#161b22; color:white; border:1px solid #30363d;}")
        m.addAction(self.t["rename"], lambda: self.rename_cat(name))
        m.addAction(self.t["delete"], lambda: self.delete_cat(name))
        m.exec(QCursor.pos())

    def rename_cat(self, old):
        new, ok = QInputDialog.getText(self, self.t["rename"], self.t["input_name"], text=old)
        if ok and new.strip() and new != old:
            n = new.strip()
            if old in self.mgr.data['categories']:
                self.mgr.data['categories'][self.mgr.data['categories'].index(old)] = n
            for v in self.mgr.data['vaults']:
                if v['category'] == old: v['category'] = n
            self.mgr.save();
            self.refresh_list()

    def delete_cat(self, name):
        if name in self.mgr.data['categories']:
            self.mgr.data['categories'].remove(name)
            for v in self.mgr.data['vaults']:
                if v['category'] == name: v['category'] = "Unclassified"
            self.mgr.save();
            self.refresh_list()

    def show_lang_menu(self):
        m = QMenu(self);
        m.setStyleSheet("QMenu{background:#161b22; color:white; border:1px solid #30363d;}")
        m.addAction("🇺🇸 English", lambda: self.set_lang("en"))
        m.addAction("🇨🇳 中文", lambda: self.set_lang("zh"))
        m.addAction("🇯🇵 日本語", lambda: self.set_lang("ja"))
        m.addAction("🇷🇺 Русский", lambda: self.set_lang("ru"))
        m.exec(self.btn_lang.mapToGlobal(self.btn_lang.rect().topRight()))

    def set_lang(self, code):
        self.mgr.data['settings']['lang'] = code
        self.mgr.save()
        self.t = I18N[code]
        self.setWindowTitle(self.t.get("title", "obvm"))
        self.btn_lang.setText(self.t["lang"])
        self.btn_export.setText(self.t["export"])
        self.btn_ref.setText(self.t["refresh"])
        self.btn_about.setText(self.t["about"])
        self.search.setPlaceholderText(self.t["search"])
        self.cat_header.setText(self.t["categories"].upper())
        self.version_label.setText(f"{self.t['version']}: {APP_VERSION}    {self.t['license']}: MIT")
        self.refresh_list()

    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle(self.t["about_title"])
        msg.setText(self.t["about_text"])
        author_btn = msg.addButton(self.t["github_author"], QMessageBox.ActionRole)
        repo_btn = msg.addButton(self.t["github_repo"], QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Ok)
        msg.exec()
        clicked = msg.clickedButton()
        if clicked == author_btn:
            QDesktopServices.openUrl(QUrl(GITHUB_AUTHOR))
        elif clicked == repo_btn:
            QDesktopServices.openUrl(QUrl(GITHUB_REPO))

    def add_cat_dialog(self):
        name, ok = QInputDialog.getText(self, self.t["new_cat_dialog"], self.t["input_name"])
        if ok and name.strip():
            n = name.strip()
            if n not in self.mgr.data['categories']:
                self.mgr.data['categories'].append(n);
                self.mgr.save();
                self.refresh_list();
                return n
        return None

    def export_md(self):
        path, _ = QFileDialog.getSaveFileName(self, self.t.get("export_title", "Export"), "", "Markdown Files (*.md)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("# Obsidian Vaults Index\n\n")
                for c in self.mgr.data['categories'] + ["Unclassified"]:
                    vs = [v for v in self.mgr.data['vaults'] if v['category'] == c]
                    if vs:
                        f.write(f"## {c}\n")
                        for v in vs:
                            f.write(f"- [{v['name']}](obsidian://open?vault={urllib.parse.quote(v['name'])}) \n")
            QMessageBox.information(self, self.t.get("export_title", "Export"), self.t["export_done"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ObsidianManagerGUI();
    window.show()
    sys.exit(app.exec())