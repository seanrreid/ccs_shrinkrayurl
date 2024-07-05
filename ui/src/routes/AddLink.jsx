import { useEffect } from 'react';
import {
    Form,
    useLoaderData,
    useActionData,
    useNavigate,
} from 'react-router-dom';
import Wrapper from '../components/Wrapper';
import Button from '../components/Button';

import styles from './form.module.css';

export const action = async ({ request }) => {
    const formData = await request.formData();
    const title = formData.get('title');
    const long_url = formData.get('long_url');
    const user_id = formData.get('user_id');
    const short_url = formData.get('short_url');

    const linkData = {
        title,
        long_url,
        short_url,
        user_id: Number(user_id),
    };

    try {
        const url = `${import.meta.env.VITE_API_URL}/urls/add`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify(linkData),
        });

        const statusCode = response.status;

        return statusCode === 200 ? true : false;
    } catch (error) {
        console.error('ERROR: ', error);
        return false;
    }
};

export async function loader() {
    try {
        const url = `${import.meta.env.VITE_API_URL}/users/current`;
        const user = await fetch(url, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
        }).then((response) => response.json());
        return { user_id: user.id };
    } catch (error) {
        console.error('ERROR:', error);
        return { error };
    }
}

const AddLink = () => {
    const navigate = useNavigate();
    const { user_id } = useLoaderData();
    const response = useActionData();

    useEffect(() => {
        return response && navigate('/links');
    }, [response, navigate]);

    return (
        <Wrapper>
            <h1>Add a Link</h1>
            <Form method="post" className={styles.form}>
                <label>
                    Title
                    <input type="text" name="title" />
                </label>
                <label>
                    URL to Shorten
                    <input type="text" name="long_url" />
                </label>
                <input type="hidden" name="user_id" value={user_id} />
                <Button type="submit">Add New Link</Button>
            </Form>
        </Wrapper>
    );
};

export default AddLink;
