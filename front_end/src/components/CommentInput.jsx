import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";

const CommentInput = ({ onSubmit, replyingTo, targetObject, userId }) => {
    const [text, setText] = useState("");

    const handleSubmit = () => {
        if (text.trim() && targetObject) {
            const contentType = targetObject.content_type;
            const objectId = targetObject.id;

            if (contentType && objectId) {
                const commentData = {
                    user_id: userId,
                    content_type: contentType,
                    object_id: objectId,
                    text: replyingTo ? `${replyingTo}, ${text}` : text,
                };
                onSubmit(commentData);
                console.log("Отправка комментария с данными:", commentData);
                setText(""); // Очистить поле ввода
            } else {
                console.error("Invalid targetObject: Missing contentType or objectId");
            }
        }
    };

    return (
        <Box mt={2}>
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
                variant="contained"
                color="primary"
                sx={{ mt: 1 }}
                onClick={handleSubmit}
            >
                Отправить
            </Button>
        </Box>
    );
};

export default CommentInput;
