请执行 LLM Wiki 收录工作流（完整规范见 05-resources/llm-wiki/schema.md）。

步骤：
1. 列出 raw/ 下所有未处理的资料文件，让用户选择本次收录哪些
2. 读取用户选中的原始资料
3. 与用户简短讨论关键收获（3-5句即可），确认理解正确
4. 在 wiki/ 下创建或更新 source-note 页面（文件名英文小写+连字符，内容中文，含完整 frontmatter）
5. 识别资料涉及的概念和实体，创建或更新对应的 wiki 页面（concept / entity / comparison 等）
6. 更新 index.md 中受影响的条目
7. 在 log.md 末尾追加操作记录，格式：`## [日期] 收录 | 资料名称`
8. 报告本次更新了哪些页面
