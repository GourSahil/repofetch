return {
  {
    "williamboman/mason.nvim",
    config = function()
      require("mason").setup()
    end,
  },

  {
    "williamboman/mason-lspconfig.nvim",
    dependencies = { "mason.nvim" },
    config = function()
      require("mason-lspconfig").setup({
        ensure_installed = {
          "pyright",
          "clangd",
          "lua_ls",
          "ts_ls",
        },
      })
    end,
  },

  {
    "neovim/nvim-lspconfig",
    dependencies = { "mason-lspconfig.nvim" },

    config = function()

      -- LSP keymaps
      vim.keymap.set("n", "K", vim.lsp.buf.hover, { desc = "Hover documentation" })
      vim.keymap.set("n", "gd", vim.lsp.buf.definition, { desc = "Go to definition" })
      vim.keymap.set("n", "gr", vim.lsp.buf.references, { desc = "Find references" })
      vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename, { desc = "Rename symbol" })

      -- enable servers (Neovim 0.11+)
      vim.lsp.enable("pyright")
      vim.lsp.enable("clangd")
      vim.lsp.enable("lua_ls")
      vim.lsp.enable("ts_ls")

    end,
  },
}
