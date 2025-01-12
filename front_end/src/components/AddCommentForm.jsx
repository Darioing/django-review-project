import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";

const AddCommentForm = ({ onSubmit, targetObject }) => {
    const [text, setText] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault(); // Предотвращаем перезагрузку страницы
        if (text.trim()) {
            onSubmit(targetObject, text.trim()); // Отправляем строку без лишних пробелов
            setText(""); // Сбрасываем поле после отправки
        } else {
            console.error("Комментарий не может быть пустым");
        }
    };

    return (
        <Box
            component="form"
            onSubmit={handleSubmit} // Используем submit для правильной обработки
            mt={2}
        >
            <TextField
                fullWidth
                variant="outlined"
                placeholder="Введите комментарий..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                multiline
                rows={2}
            />
            <Button
                type="submit" // Меняем тип на "submit" для стандартного поведения формы
                variant="contained"
                color="primary"
                sx={{ mt: 1 }}
            >
                Отправить
            </Button>
        </Box>
    );
};

export default AddCommentForm;
