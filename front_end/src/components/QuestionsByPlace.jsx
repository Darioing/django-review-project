import React, { useEffect, useState } from "react";
import { Box, Card, CardContent, Typography, Avatar, Button } from "@mui/material";

const QuestionsByPlace = ({ placeId, slug }) => {
    const [questions, setQuestions] = useState([]);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/review/questions/?place_id=${placeId}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Ошибка при загрузке вопросов");
                }
                return response.json();
            })
            .then((data) => setQuestions(data))
            .catch((error) => console.error("Ошибка загрузки вопросов:", error));
    }, [placeId]);

    return (
        <Box display="flex" flexDirection="column" gap={2}>
            {questions.length > 0 ? (
                questions.map((question) => (
                    <Card key={question.id} sx={{ mb: 2, p: 2 }}>

                        <CardContent>
                            {/* Отображение пользователя */}
                            <Box display="flex" alignItems="center" mb={2}>
                                <Avatar
                                    src={question.user_avatar || "/static/images/default_avatar.png"}
                                    alt={question.user_fio}
                                    sx={{ width: 50, height: 50, mr: 2 }}
                                />
                                <Typography variant="body2" fontWeight="bold">
                                    {question.user_fio}
                                </Typography>
                            </Box>
                            {/* Текст вопроса */}
                            <Typography variant="body1">{question.text}</Typography>
                            {/* Дата создания */}
                            <Typography variant="caption" color="textSecondary">
                                {new Date(question.created_at).toLocaleDateString()}
                            </Typography>
                        </CardContent>
                    </Card>
                ))
            ) : (
                <Typography variant="body2" color="textSecondary">
                    Вопросов к этому заведению пока нет.
                </Typography>
            )}
        </Box>
    );
};

export default QuestionsByPlace;
