return {
  "akinsho/bufferline.nvim",
  dependencies = { "nvim-tree/nvim-web-devicons" },

  config = function()
    require("bufferline").setup({
      options = {
        mode = "buffers",
        separator_style = "slant",

        diagnostics = "nvim_lsp",

        offsets = {
          {
            filetype = "neo-tree",
            text = "File Explorer",
            highlight = "Directory",
            separator = true,
          },
        },
      },
    })
  end,
}
