import React, { useEffect, useState } from "react";
import {
    Box,
    Typography,
    Card,
    CardContent,
    Avatar,
    Divider,
    Button,
} from "@mui/material";
import CommentThread from "./CommentThread";
import AddCommentForm from "./AddCommentForm";

const QuestionsByPlace = ({ placeId }) => {
    const [questions, setQuestions] = useState([]);
    const [comments, setComments] = useState({});
    const [activeQuestionId, setActiveQuestionId] = useState(null);
    const [replyTarget, setReplyTarget] = useState(null); // Объект, к которому добавляется комментарий

    // Загрузка вопросов
    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/review/questions/?place_id=${placeId}`
                );
                const data = await response.json();
                setQuestions(data);
            } catch (error) {
                console.error("Ошибка при загрузке вопросов:", error);
            }
        };

        fetchQuestions();
    }, [placeId]);

    // Загрузка комментариев для конкретного вопроса
    const fetchComments = async (questionId) => {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/review/comments/${questionId}/by-object/?content_type=12`
            );
            const data = await response.json();
            setComments((prev) => ({ ...prev, [questionId]: data }));
        } catch (error) {
            console.error("Ошибка при загрузке комментариев:", error);
        }
    };


    // Добавление комментария
    const handleAddComment = async (targetObject, commentText) => {
        const data = {
            user_id: localStorage.getItem("user_id"),
            content_type: targetObject.self_content_type,
            object_id: targetObject.id,
            text: commentText,
        };

        try {
            const response = await fetch(`http://127.0.0.1:8000/review/comments/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access")}`,
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                const newComment = await response.json();

                setComments((prev) => {
                    const updatedComments = { ...prev };

                    if (targetObject.self_content_type === 12) {
                        // Добавление в корневой уровень
                        updatedComments[targetObject.id] = [
                            ...(updatedComments[targetObject.id] || []),
                            newComment,
                        ];
                    } else {
                        // Добавление в ветвь комментариев
                        const updateBranch = (comments) => {
                            return comments.map((comment) => {
                                if (comment.id === targetObject.id) {
                                    return {
                                        ...comment,
                                        children: [...(comment.children || []), newComment],
                                    };
                                } else if (comment.children && comment.children.length > 0) {
                                    return {
                                        ...comment,
                                        children: updateBranch(comment.children),
                                    };
                                }
                                return comment;
                            });
                        };

                        updatedComments[targetObject.object_id] = updateBranch(
                            updatedComments[targetObject.object_id] || []
                        );
                    }

                    return updatedComments;
                });
            } else {
                console.error("Ошибка при добавлении комментария:", await response.text());
            }
        } catch (error) {
            console.error("Ошибка при отправке комментария:", error);
        }
    };

    return (
        <Box mt={4}>
            {questions.map((question) => (
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

                        <Divider sx={{ mb: 2 }} />

                        {/* Текст вопроса */}
                        <Typography variant="body1" gutterBottom>
                            {question.text}
                        </Typography>

                        {/* Дата создания */}
                        <Typography
                            variant="caption"
                            color="textSecondary"
                            display="block"
                            mt={2}
                        >
                            {new Date(question.created_at).toLocaleDateString()}
                        </Typography>

                        {/* Кнопка отображения комментариев */}
                        <Button
                            variant="text"
                            color="primary"
                            sx={{ mt: 1 }}
                            onClick={() => {
                                setActiveQuestionId(
                                    activeQuestionId === question.id ? null : question.id
                                );
                                fetchComments(question.id);
                            }}
                        >
                            {activeQuestionId === question.id
                                ? "Скрыть комментарии"
                                : "Показать комментарии"}
                        </Button>

                        {/* Кнопка добавления комментария */}
                        <Button
                            variant="text"
                            color="secondary"
                            sx={{ mt: 1 }}
                            onClick={() => setReplyTarget(question)}
                        >
                            Ответить
                        </Button>

                        {/* Форма добавления комментария */}
                        {replyTarget && replyTarget.id === question.id && (
                            <AddCommentForm
                                onSubmit={(target, text) => handleAddComment(target, text)}
                                targetObject={replyTarget}
                                onCancel={() => setReplyTarget(null)}
                            />
                        )}

                        {/* Отображение комментариев */}
                        {activeQuestionId === question.id && (
                            <CommentThread
                                comments={comments[question.id] || []}
                                onReply={(comment) => setReplyTarget(comment)}
                                replyTarget={replyTarget}
                                onCancelReply={() => setReplyTarget(null)}
                                onAddComment={(target, text) => handleAddComment(target, text)}
                            />
                        )}
                    </CardContent>
                </Card>
            ))}
        </Box>
    );
};

export default QuestionsByPlace;
