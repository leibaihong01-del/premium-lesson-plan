# Codex C盘迁移至D盘：第二阶段迁移方案（设计稿）

日期：2026-08-02    阶段：Phase 2 方案设计（未执行）    目标：D:\AI\Codex

## 一、目标目录结构

```text
D:\AI\Codex
├── Core\config           # Codex 配置、CCSwitch 配置
├── Core\plugins          # 插件
├── Core\extensions       # 扩展
├── UserData\sessions     # 会话
├── UserData\history      # 历史/归档会话
├── UserData\memory       # 记忆、sqlite
├── UserData\logs         # 日志
├── Cache                 # codex-runtimes、模型/运行时缓存
├── Workspace\CourseAgent # 项目工作区（可联接现有D盘工作区）
├── Skills                # skills
├── Temp                  # TEMP/TMP
├── PythonEnv             # Python 运行时
├── NodeCache             # Node/npm 缓存
└── Backup                # 迁移前备份
```

## 二、迁移映射表

| C盘路径 | D盘目标 | 方式 | 说明 |
|---|---|---|---|
| C:\Users\leibaihong\.codex | D:\AI\Codex\UserData\codex-home | 复制+目录联接（原目录改名 .codex.bak） | CODEX_HOME 指向目标，保留凭据一致性 |
| C:\Users\leibaihong\.cache\codex-runtimes | D:\AI\Codex\Cache\codex-runtimes | 复制+目录联接 | 更新工作区依赖路径或直接联接 |
| C:\Users\leibaihong\AppData\Roaming\Codex | D:\AI\Codex\UserData\RoamingCodex | 复制+目录联接 | 桌面应用数据 |
| C:\Users\leibaihong\AppData\Local\Codex | D:\AI\Codex\UserData\LocalCodex | 复制+目录联接 | 本地应用数据 |
| C:\Users\leibaihong\AppData\Local\Temp | D:\AI\Codex\Temp | 设置TEMP/TMP环境变量；原目录改名.bak | 迁移时机建议在退出应用后 |
| C:\Users\leibaihong\.codex\skills | D:\AI\Codex\Skills | 随 codex-home 迁移即可 | 保持相对结构 |
| AppData\Local\com.ccswitch.desktop | D:\AI\Codex\Core\ccswitch-local | 复制+目录联接 | CCSwitch本地配置 |
| AppData\Roaming\com.ccswitch.desktop | D:\AI\Codex\Core\ccswitch-roaming | 复制+目录联接 | CCSwitch配置/日志 |
| C:\Program Files\WindowsApps\OpenAI.Codex* | 不迁移 | 禁止改动 | 系统管理 |
| npm/pip 缓存（如存在） | D:\AI\Codex\NodeCache、Cache\pip | 设置环境变量 npm_config_cache、PIP_CACHE_DIR | 后续生效 |

## 三、环境变量方案

用户变量（user environment）：

```text
CODEX_HOME=D:\AI\Codex\UserData\codex-home
TEMP=D:\AI\Codex\Temp
TMP=D:\AI\Codex\Temp
NPM_CONFIG_CACHE=D:\AI\Codex\NodeCache
PIP_CACHE_DIR=D:\AI\Codex\Cache\pip
```

若 Codex 桌面应用不支持 CODEX_HOME，则采用“目录联接”保证旧路径仍可用。

## 四、目录联接方案

原则：不删除C盘数据；原目录先改名 `.bak` 备份，再建立 Junction（`mklink /J`）指向D盘目标。

候选联接：

- C:\Users\leibaihong\.codex → D:\AI\Codex\UserData\codex-home
- C:\Users\leibaihong\.cache\codex-runtimes → D:\AI\Codex\Cache\codex-runtimes
- AppData\Roaming\Codex、AppData\Local\Codex → UserData 对应目录
- com.ccswitch.desktop（Local/Roaming）→ Core\ccswitch-*

需管理员权限；联接建立前必须完成备份与验证。

## 五、备份策略

1. 迁移前将敏感文件复制到 D:\AI\Codex\Backup\2026-08-02\：auth.json、.codex-global-state.json、config.toml、sqlite文件、ccswitch配置；
2. 原C盘目录统一改名 `.bak`（不删除）；
3. 迁移后先验证，验证通过并稳定运行一段时间后再决定是否清理 `.bak`。

## 六、CCSwitch配置同步

- 复制配置后保留原目录（Junction）；
- 确认 DeepSeek API 配置路径与密钥（环境变量）不受影响；
- 验证 cc-switch-model-catalog.json 与 API 配置可读取。

## 七、执行顺序（Phase 3，待确认后执行）

1. 备份敏感文件；
2. 复制 .codex、codex-runtimes、Roaming/Local Codex、CCSwitch数据到D盘；
3. 设置用户环境变量（TEMP/TMP/CODEX_HOME/缓存目录）；
4. 原目录改名 .bak，建立Junction；
5. 重启Codex与CCSwitch验证；
6. 运行CourseAgent与AGENTS.md读取验证；
7. 验证通过后进入Phase 6输出报告。

## 八、验证清单（对应Phase 6）

- [ ] Codex启动正常；
- [ ] CourseAgent正常；
- [ ] AGENTS.md正常读取；
- [ ] skills正常；
- [ ] CCSwitch正常；
- [ ] DeepSeek API配置正常；
- [ ] 新任务数据写入D盘；
- [ ] C盘空间释放（Temp、codex-runtimes等）。

## 九、风险与限制

1. WindowsApps 程序安装目录不可迁移；
2. auth/全局状态迁移失败可能导致登录失效（需备份+回滚）；
3. Temp 迁移需在退出应用/重启后进行；
4. .config 权限受限，本次未纳入；
5. 目录联接需要管理员权限；
6. 迁移期间 Codex/CCSwitch 必须退出，避免文件占用。

## 十、结论

本方案为设计稿，未执行任何迁移、删除或环境变量修改；Phase 3 执行需人工确认并具备管理员权限。
