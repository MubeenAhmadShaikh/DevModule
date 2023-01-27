from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from core import models, database, schemas

# To create a skill
def create_skill(name, description, db, current_user):
    for skill in current_user.skill:
        if skill.name == name.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already have this skill in your profile",
            )
    create_skill = models.Skill(
        name=name.lower(), description=description, owner_id=current_user.id
    )
    db.add(create_skill)
    db.commit()
    db.refresh(create_skill)
    return create_skill


# To update a skill
def update_skill(id, name, description, db):
    update_skill = db.query(models.Skill).filter(models.Skill.id == id)
    if not update_skill.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such skill exist"
        )
    update_skill.update({"name": name, "description": description})
    db.commit()
    return "Updated skill"


# To delete a skill
def delete_skill(id, db):
    delete_skill = db.query(models.Skill).filter(models.Skill.id == id)
    if not delete_skill.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such skill exist"
        )
    delete_skill.delete()
    db.commit()
    return "Deleted skill"


# To get single skill
def view_single_skill(id, db):
    single_skill = db.query(models.Skill).filter(models.Skill.id == id).first()
    if not single_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such skill exist"
        )
    return single_skill


# To view all skill
def view_all_skills(db):
    all_skills = db.query(models.Skill).all()
    return all_skills
