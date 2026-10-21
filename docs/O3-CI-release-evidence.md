# O3：CI 门禁与可追踪发布证据

更新日期：2026-10-21  
项目：IssueScope（GitHub: [S1mpleWind/IssueScope](https://github.com/S1mpleWind/IssueScope)）

## 目标

用自动化检查保护 `main`，让变更通过 PR 和 CI 后再进入主分支；发布包提供版本、构建号、源码 commit 与校验和，便于从运行产物追溯源码。

## GitHub 分支规则

已通过 `gh api` 检查仓库 ruleset `main-branch`（ID `25532883`）：规则处于 active，目标是默认分支。要求 PR、至少 1 个 approval 和 `ci` 状态检查；禁止删除分支与 non-fast-forward 更新。规则详情可在 [GitHub ruleset](https://github.com/S1mpleWind/IssueScope/settings/rules/25532883) 查看。

## CI 门禁演练

PR [#51](https://github.com/S1mpleWind/IssueScope/pull/51) 演示了红灯到绿灯流程：

1. 提交一个故意写错期望值的前端测试。Actions run [39570727566](https://github.com/S1mpleWind/IssueScope/actions/runs/39570727566) 按预期失败；日志显示后端依赖安装与后端测试先通过，前端测试失败。
2. 将期望值改成 UI 实际使用的“源码”。Actions run [39570870332](https://github.com/S1mpleWind/IssueScope/actions/runs/39570870332) 的 `ci` 成功。
3. PR #51 目前仍等待一位 reviewer 审批，未合并。

## 发布追踪实现

PR [#52](https://github.com/S1mpleWind/IssueScope/pull/52) 加入以下内容：

- `GET /api/version`：返回 `version`、`build`、`commit`。开发环境缺少元数据时返回 `0.1.0`、`dev`、`unknown`。
- `.github/workflows/release.yml`：收到 `vX.Y.Z` tag 后先校验格式，并确认 tag commit 属于 `main` 历史；然后运行后端和前端检查、构建前端、生成含 `BUILD_INFO.json` 的 tar.gz 与 SHA-256 文件，并发布 GitHub Release。
- `scripts/trace.sh`：从 release tarball 读取并输出版本、构建号与源码 commit。

PR #52 的 GitHub Actions run [39571353021](https://github.com/S1mpleWind/IssueScope/actions/runs/39571353021) 已成功，包含后端依赖安装和测试、前端依赖安装、lint、测试、生产构建。

本地验证结果：

- 后端：177 passed，5 skipped。
- 前端：lint 通过，7 个测试通过，生产构建通过。
- 归档演练：从样例 tar.gz 成功读取版本、构建号、commit。

## 当前状态与后续

PR #51 和 #52 均为 open，CI 均通过，但 GitHub 规则要求的 approval 尚未满足，所以尚未合并。没有创建 tag 或 GitHub Release。待 PR #52 经审批合并到 `main` 后，再对主分支提交创建 `vX.Y.Z` tag，release workflow 才会生成正式发布包与校验和。PR #51 可单独审查并决定是否合并其新增测试。

GitHub 证据也已通过 `gh pr comment` 记入 [PR #51 评论](https://github.com/S1mpleWind/IssueScope/pull/51#issuecomment-6311846624) 和 [PR #52 评论](https://github.com/S1mpleWind/IssueScope/pull/52#issuecomment-6311847332)。
