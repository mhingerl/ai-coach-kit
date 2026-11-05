# Loading this kit (for Claude)

The athlete pasted this repository's link and asked you to set them up as their coach. This file says how to load the kit so the setup instructions can do their job.

1. **Get the files exactly as written.** Clone the repository into your workspace (`git clone --depth 1 https://github.com/<owner>/<repo>.git`, owner and repo from the link the athlete pasted), or attach it if you have a tool for adding repositories, and read the files from disk. Don't rely on a summarized web page: the dashboard template is code and has to be used unchanged. If you can't clone, fetch each file's raw contents from the repository and check that nothing was shortened.
2. **Keep them where later chats can see them.** If you're in a Claude Project and can write project documents, save the five files from `kit/` into the project under the same names. Otherwise keep them available in this conversation and, at the end of setup, give the athlete the documents to add to a Project.
3. **Follow `kit/ai-coach-setup-prompt.md`.** Its "For you" part is for the athlete; everything below its line is your instructions, starting with the interview. The other four files are used during setup as it describes (library, check-in skill template, dashboard template, exercise catalogue).
4. **Tell the athlete what's happening** in one or two sentences before starting the interview: what you loaded, roughly how long setup takes, and that they can stop and continue in a later chat.

The kit version is the date in the one-line `VERSION` file (also at the end of `kit/ai-coach-setup-prompt.md`). Changes are listed in `CHANGELOG.md`. For a later update check, read only `VERSION` first; fetch `CHANGELOG.md` and the files an entry names only when it differs.
