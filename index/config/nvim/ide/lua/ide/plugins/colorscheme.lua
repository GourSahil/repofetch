return {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,

    config = function()
      require("catppuccin").setup({
        flavour = "mocha", -- latte, frappe, macchiato, mocha

        integrations = {
          treesitter = true,
          gitsigns = true,
          telescope = true,
          bufferline = true,
          neotree = true,
        },
      })

      vim.cmd.colorscheme("catppuccin")
    end,
  },
}
