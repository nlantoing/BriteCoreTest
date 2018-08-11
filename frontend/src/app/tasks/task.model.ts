export class Task {
    constructor(
	private id: number,
	public title: string,
	public description: string,
	public priority: number,
	public target_date: Date,
	public user_id: number,
	public project_id: number,
	public category_id: number
    ){}
       
}
