import { useLoaderData } from 'react-router-dom';
import Wrapper from '../components/Wrapper';
import LinkList from '../components/LinkList';

export async function loader() {
    try {
        const url = `${import.meta.env.VITE_API_URL}/urls/`;
        const linkList = await fetch(url, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
        }).then((response) => response.json());
        if (!Array.isArray(linkList)) {
            throw Error('Not an array of links');
        }
        return { linkList };
    } catch (error) {
        console.error("ERROR:", error);
        return { error }
    }
}

const Links = () => {
     const { linkList } = useLoaderData();
    return (
        <Wrapper>
            <h1>View Links</h1>
            <LinkList linkList={linkList} />
        </Wrapper>
    );
};

export default Links;
