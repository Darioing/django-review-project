import { Box, Grid2, Typography } from "@mui/material";
import React from "react";

const Footer = () => {
    return (
        <Box
            sx={{
                width: "100%",
                bgcolor: "background.default",
                borderTop: 1,
                borderColor: "divider",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                padding: "8px", // Уменьшенные отступы
                position: "relative",
                mt: "auto", // Обеспечивает фиксацию внизу страницы
                '@media (max-width: 600px)': {
                    padding: "4px",
                },
            }}
        >
            <Grid2 container spacing={1} sx={{ maxWidth: "100%", textAlign: "center" }}>
                <Grid2 item xs={12}>
                    <Typography variant="body2" sx={{ fontSize: "14px", lineHeight: "1.4" }}>
                        Проект создан для дипломной работы и не направлен на извлечение прибыли.
                    </Typography>
                </Grid2>
            </Grid2>
            <Box sx={{ textAlign: "center", marginTop: "4px" }}>
                <Typography variant="caption" color="text.secondary" sx={{ fontSize: "12px" }}>
                    © 2025 Ваш проект
                </Typography>
            </Box>
        </Box>
    );
};

export default Footer;
