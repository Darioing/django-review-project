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
import VoteControl from "./VoteControl";

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
            {questions.length === 0 ? (
                <Typography
                    variant="h6"
                    color="textSecondary"
                    align="center"
                    sx={{ mt: 4 }}
                >
                    Для данного заведения еще нет вопросов!
                </Typography>
            ) : (
                questions.map((question) => (
                    <Card
                        key={question.id}
                        sx={{ mb: 2, p: 2, display: "flex", alignItems: "flex-start" }}
                    >
                        {/* Компонент с голосованием и вопросом */}
                        <Box display="flex" flexDirection="row" flex={1}>
                            {/* Блок голосования */}
                            <Box
                                display="flex"
                                flexDirection="column"
                                alignItems="center"
                                justifyContent="flex-start"
                                sx={{ mr: 2, minWidth: 50 }}
                            >
                                <VoteControl
                                    contentType={question.self_content_type}
                                    objectId={question.id}
                                    onVote={(vote) => console.log("New vote:", vote)}
                                />
                            </Box>

                            {/* Основной блок вопроса */}
                            <Box flex={1}>
                                <CardContent sx={{ p: 0 }}>
                                    {/* Отображение пользователя */}
                                    <Box display="flex" alignItems="center" mb={2}>
                                        <Avatar
                                            src={
                                                question.user_avatar ||
                                                "/static/images/default_avatar.png"
                                            }
                                            alt={question.user_fio}
                                            sx={{ width: 50, height: 50, mr: 2 }}
                                        />
                                        <Typography variant="body2" fontWeight="bold">
                                            {question.user_fio}
                                        </Typography>
                                    </Box>
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

                                    {/* Кнопки */}
                                    <Box mt={2}>
                                        <Button
                                            variant="text"
                                            color="primary"
                                            sx={{
                                                mr: 2,
                                                display: question.comment_count > 0
                                                    ? "inline-flex"
                                                    : "none",
                                            }}
                                            onClick={() => {
                                                setActiveQuestionId(
                                                    activeQuestionId === question.id
                                                        ? null
                                                        : question.id
                                                );
                                                fetchComments(question.id);
                                            }}
                                        >
                                            {activeQuestionId === question.id
                                                ? "Скрыть комментарии"
                                                : "Показать комментарии"}
                                        </Button>
                                        <Button
                                            variant="text"
                                            color="primary"
                                            onClick={() =>
                                                setReplyTarget(
                                                    replyTarget?.id === question.id &&
                                                        replyTarget?.self_content_type ===
                                                        question.self_content_type
                                                        ? null // Скрываем форму, если она уже открыта для этого вопроса
                                                        : question // Устанавливаем target, если форма ещё не открыта
                                                )
                                            }
                                        >
                                            {replyTarget?.id === question.id
                                                ? "Отменить"
                                                : "Ответить"}
                                        </Button>
                                    </Box>
                                </CardContent>

                                {/* Форма добавления комментария */}
                                {replyTarget && replyTarget.id === question.id && (
                                    <AddCommentForm
                                        onSubmit={(target, text) =>
                                            handleAddComment(target, text)
                                        }
                                        targetObject={replyTarget}
                                        onCancel={() => setReplyTarget(null)}
                                    />
                                )}

                                {/* Отображение комментариев */}
                                {activeQuestionId === question.id && (
                                    <Box mt={2}>
                                        <CommentThread
                                            comments={comments[question.id] || []}
                                            onReply={(comment) => setReplyTarget(comment)}
                                            replyTarget={replyTarget}
                                            onCancelReply={() => setReplyTarget(null)}
                                            onAddComment={(target, text) =>
                                                handleAddComment(target, text)
                                            }
                                        />
                                    </Box>
                                )}
                            </Box>
                        </Box>
                    </Card>
                ))
            )}
        </Box>
    );

};

export default QuestionsByPlace;
