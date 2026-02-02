import { useEffect, useState } from "react";
import axios from "axios";
import "./UserAvatar.css";

function UserAvatar() {

    const [bioPic,setBioPic] = useState(null)
    const [open,setOpen] = useState(false)

    const token = localStorage.getItem("token")

    useEffect(() => {
    axios.get("https://task-app-project-6uvh.onrender.com/api/profile/", {
      headers: { Authorization: `Bearer ${token}` },
    })

    .then(res => setBioPic(res.data.bio_pic));
    }, [token]);

    const uploadImage = (file) => {

        if(!file) 
            return;

        const formData = new FormData();
        formData.append("bio_pic", file);

        axios.put("https://task-app-project-6uvh.onrender.com/api/profile/bio-pic/",
        formData,
        {
            headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
            },
        }
        )

        .then(res => {
        setBioPic(res.data.bio_pic);
        setOpen(false);
        });
    };

    const deleteImage = () => {

        axios.delete("https://task-app-project-6uvh.onrender.com/api/profile/bio-pic/delete/",
        {
            headers: { Authorization: `Bearer ${token}` },
        }

        )
        .then(() => {
        setBioPic(null);
        setOpen(false);
        });

    };

      return (
        <div className="avatar-wrapper">

        <img src={bioPic ? `https://task-app-project-6uvh.onrender.com${bioPic}` : "/default-icon.svg"} alt="profile" className="avatar-icon"
            onClick={() => setOpen(!open)} />

        {open && (
        
        <div className="avatar-popup">

        <img src={bioPic ? `https://task-app-project-6uvh.onrender.com${bioPic}` : "/default-icon.svg"} alt="preview" className="avatar-preview"/>

            <label>

                <input type="file" hidden onChange={(e) => uploadImage(e.target.files[0])} />
                <div className="upload-btn">Update</div>

            </label>

            {bioPic && (
                <button className="delete-btn" onClick={deleteImage}>Delete</button>
            )}

            </div>
        )}

        </div>
    );
}

export default UserAvatar;