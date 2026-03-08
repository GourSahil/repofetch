return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  event = { "BufReadPost", "BufNewFile" },

  config = function()
    local configs = require("nvim-treesitter.config")

    configs.setup({
      ensure_installed = {
        "lua",
        "python",
        "c",
        "cpp",
        "javascript",
        "html",
        "css"
      },

      highlight = {
        enable = true,
      },

      indent = {
        enable = true,
      },
    })
  end,
}

