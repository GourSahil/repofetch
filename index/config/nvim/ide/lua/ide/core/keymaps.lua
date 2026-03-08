vim.g.mapleader = " "

local keymap = vim.keymap

--------------------------------------------------
-- Basic actions
--------------------------------------------------

keymap.set("n", "<leader>w", "<cmd>w<CR>", { desc = "Save file" })
keymap.set("n", "<leader>q", "<cmd>q<CR>", { desc = "Quit window" })
keymap.set("n", "<leader>nh", "<cmd>nohlsearch<CR>", { desc = "Clear search highlight" })

--------------------------------------------------
-- Window navigation
--------------------------------------------------

keymap.set("n", "<C-h>", "<C-w>h", { desc = "Move window left" })
keymap.set("n", "<C-l>", "<C-w>l", { desc = "Move window right" })
keymap.set("n", "<C-j>", "<C-w>j", { desc = "Move window down" })
keymap.set("n", "<C-k>", "<C-w>k", { desc = "Move window up" })

keymap.set("n", "<leader>h", "<C-w>h", { desc = "Focus left window" })
keymap.set("n", "<leader>l", "<C-w>l", { desc = "Focus right window" })
keymap.set("n", "<leader>j", "<C-w>j", { desc = "Focus lower window" })
keymap.set("n", "<leader>k", "<C-w>k", { desc = "Focus upper window" })

--------------------------------------------------
-- Neo-tree
--------------------------------------------------

keymap.set("n", "<leader>e", "<cmd>Neotree toggle<CR>", { desc = "Toggle explorer" })

--------------------------------------------------
-- Buffer control (THIS fixes your issue)
--------------------------------------------------
-- Close current file properly
keymap.set("n", "<leader>c", function()
  require("mini.bufremove").delete(0, false)
end, { desc = "Close buffer" })

-- Force close
keymap.set("n", "<leader><C-c>", function()
  require("mini.bufremove").delete(0, true)
end, { desc = "Force close buffer" })

--------------------------------------------------
-- Bufferline tabs
--------------------------------------------------

keymap.set("n", "<Tab>", "<cmd>BufferLineCycleNext<CR>", { desc = "Next tab" })
keymap.set("n", "<S-Tab>", "<cmd>BufferLineCyclePrev<CR>", { desc = "Previous tab" })

--------------------------------------------------
-- Diagnostics
--------------------------------------------------

keymap.set("n", "[d", vim.diagnostic.goto_prev, { desc = "Previous diagnostic" })
keymap.set("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })
keymap.set("n", "<leader>d", vim.diagnostic.open_float, { desc = "Show diagnostic" })

--------------------------------------------------
-- Project root
--------------------------------------------------

keymap.set("n", "<leader>r", function()
  local path = vim.fn.expand("%:p:h")
  vim.cmd("cd " .. path)
end, { desc = "Set file directory as root" })
