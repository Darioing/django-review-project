import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";

const AddCommentForm = ({ onSubmit, targetObject, onCancel }) => {
    const [text, setText] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (text.trim()) {
            onSubmit(targetObject, text.trim());
            setText(""); // Сбрасываем поле после отправки
            onCancel(); // Закрываем форму после успешной отправки
        } else {
            console.error("Комментарий не может быть пустым");
        }
    };

    return (
        <Box
            component="form"
            onSubmit={handleSubmit}
            mt={2}
            sx={{ mb: 2 }}
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
            <Box mt={1} display="flex" justifyContent="space-between">
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                >
                    Отправить
                </Button>
                <Button
                    variant="text"
                    color="secondary"
                    onClick={onCancel} // Закрытие формы по кнопке
                >
                    Отмена
                </Button>
            </Box>
        </Box>
    );
};

export default AddCommentForm;
