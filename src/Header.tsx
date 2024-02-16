import { Box } from "@mui/material";
// import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

export default function Header() {
  return (
    <>
      <Box
        sx={{
          //   borderBottom: 1,
          //   borderRight: 2,

          display: "flex",
          borderColor: "#66BB6A",
          // background: "#2F684D",
          justifyContent: "space-between",
          alignItems: "center",
          // boxShadow: "0px 0px 16px 0px #51CC76",
          height: "15vh",
          width: "100vw",
        }}
      >
        <svg
          width="615"
          height="56"
          viewBox="0 0 615 56"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g filter="url(#filter0_d_4_16)">
            <path
              d="M600 34H434.234L396.096 14H3.57628e-07"
              stroke="#368A57"
              stroke-width="5"
            />
          </g>
          <defs>
            <filter
              id="filter0_d_4_16"
              x="-15"
              y="0.5"
              width="630"
              height="55"
              filterUnits="userSpaceOnUse"
              color-interpolation-filters="sRGB"
            >
              <feFlood flood-opacity="0" result="BackgroundImageFix" />
              <feColorMatrix
                in="SourceAlpha"
                type="matrix"
                values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                result="hardAlpha"
              />
              <feOffset dy="4" />
              <feGaussianBlur stdDeviation="7.5" />
              <feComposite in2="hardAlpha" operator="out" />
              <feColorMatrix
                type="matrix"
                values="0 0 0 0 0.404444 0 0 0 0 0.933333 0 0 0 0 0.429334 0 0 0 1 0"
              />
              <feBlend
                mode="normal"
                in2="BackgroundImageFix"
                result="effect1_dropShadow_4_16"
              />
              <feBlend
                mode="normal"
                in="SourceGraphic"
                in2="effect1_dropShadow_4_16"
                result="shape"
              />
            </filter>
          </defs>
        </svg>
        <Box sx={{ display: "flex", alignItems: "center", gap: 3, mt: "12px" }}>
          <img src="5.png" width={"80px"} height={"80px"}></img>
          <Typography
            component="h2"
            variant="h4"
            align="center"
            noWrap
            sx={{ flex: 1, color: "#66BB6A", fontWeight: "bold" }}
          >
            New AI Assitant
          </Typography>
        </Box>
        <svg
          width="610"
          height="56"
          viewBox="0 0 610 56"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g filter="url(#filter0_d_4_19)">
            <path
              d="M15 34H180.766L218.904 14H615"
              stroke="#368A57"
              stroke-width="5"
            />
          </g>
          <defs>
            <filter
              id="filter0_d_4_19"
                x="0" 
              y="0.5"
              width="630"
              height="55"
              filterUnits="userSpaceOnUse"
              color-interpolation-filters="sRGB"
            >
              <feFlood flood-opacity="0" result="BackgroundImageFix" />
              <feColorMatrix
                in="SourceAlpha"
                type="matrix"
                values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                result="hardAlpha"
              />
              <feOffset dy="4" />
              <feGaussianBlur stdDeviation="7.5" />
              <feComposite in2="hardAlpha" operator="out" />
              <feColorMatrix
                type="matrix"
                values="0 0 0 0 0.404444 0 0 0 0 0.933333 0 0 0 0 0.429334 0 0 0 1 0"
              />
              <feBlend
                mode="normal"
                in2="BackgroundImageFix"
                result="effect1_dropShadow_4_19"
              />
              <feBlend
                mode="normal"
                in="SourceGraphic"
                in2="effect1_dropShadow_4_19"
                result="shape"
              />
            </filter>
          </defs>
        </svg>
      </Box>
    </>
  );
}
